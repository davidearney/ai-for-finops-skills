---
name: md-to-gdoc
description: Convert a markdown file to a Google Doc with proper table formatting, headings, and inline styles
---

# Markdown to Google Doc

Convert a markdown file into a new Google Doc with proper table formatting (borders, headers, column alignment), headings, inline styles, and links. Uses an HTML intermediary and browser copy-paste to preserve rich formatting that no API approach matches.

## ROLE

Act as a document conversion assistant. Execute the workflow silently and report the result. No commentary needed between steps unless something fails.

## INPUTS

- **Markdown file path** (required): absolute path to the `.md` file
- **Drive folder URL** (required): Google Drive folder URL where the new doc should be created
- **Document title** (optional): title for the Google Doc. Defaults to first H1 in the markdown, then filename stem.

If the markdown file path or Drive folder URL is not provided, ask before proceeding.

## CONSTANTS

- **Converter script**: `/Users/matthewcowsert/.claude/skills/md-to-gdoc/convert_md_to_html.py`
- **HTML output path**: `/tmp/md-to-gdoc-output.html`
- **Port range**: 8100-8999 (random selection, retry on conflict)

## PROCESS

Execute these 10 steps sequentially. If any step fails, see ERROR HANDLING before retrying.

---

### Step 1: Validate Inputs

1. Confirm the `.md` file exists at the given path. If not, stop and report.
2. Extract the Google Drive folder ID from the URL using regex: `folders\/([a-zA-Z0-9_-]+)`. This handles URLs with `/u/0/`, query parameters, and trailing slashes.
3. Determine the document title:
   - Use the user-provided title if given
   - Otherwise, read the markdown file and extract the first H1 (`# Title`)
   - If no H1, use the filename stem (e.g., `my-analysis.md` becomes `my-analysis`)

### Step 2: Convert Markdown to HTML

Run the converter script:

```bash
python3 /Users/matthewcowsert/.claude/skills/md-to-gdoc/convert_md_to_html.py "{MD_PATH}" /tmp/md-to-gdoc-output.html "{TITLE}"
```

Verify the output file exists and is non-empty. The script handles:
- ASCII code-block tables with `+`/`-`/`|` separators and multi-line continuation cells
- Standard markdown pipe tables (`| col1 | col2 |`)
- Gap analysis blocks with `[covered]`/`[partial]`/`[gap]` color-coded markers
- Inline markdown: bold, italic, inline code, links
- Full HTML document with embedded CSS styles

### Step 3: Start HTTP Server

Google Docs needs rich HTML from the clipboard. Serve the HTML locally so Chrome can render it.

1. Pick a random port between 8100 and 8999.
2. Start the server in background:
   ```bash
   python3 -m http.server {PORT} --directory /tmp &
   ```
3. Store the PID.
4. If the port is in use, retry with a different random port (up to 3 attempts).

### Step 4: Get Browser Context

1. Call `tabs_context_mcp` to get available tabs.
2. Create a new tab with `tabs_create_mcp` for this workflow.

### Step 5: Open HTML in Chrome and Copy

1. Navigate the tab to `http://localhost:{PORT}/md-to-gdoc-output.html`.
2. Wait 2 seconds for rendering.
3. Click the body of the page.
4. Select All (Cmd+A), then Copy (Cmd+C).
5. The clipboard now contains rich HTML with real table elements.

### Step 6: Create Google Doc

1. Navigate to: `https://docs.new`
2. Wait for the document to fully load (wait 5 seconds, then screenshot to confirm).
3. If prompted to sign in, stop and tell the user to authenticate in Chrome first.
4. Extract the document ID from the browser URL using regex: `document/d/([a-zA-Z0-9_-]+)/`. Store it for the move step later.

### Step 7: Set Title

1. Find and click the "Untitled document" title area at the top of the page.
2. Select all existing text (Cmd+A).
3. Type the document title.
4. Press Enter or click into the document body to confirm.

### Step 8: Paste Content

1. Click into the document body area.
2. Paste (Cmd+V).
3. Wait 5 seconds for Google Docs to process the rich content.
4. Take a screenshot to verify tables rendered with borders and proper formatting.
5. If the paste appears empty or shows only plain text, see ERROR HANDLING.

### Step 9: Move Doc to Target Folder

Move the document from My Drive root to the user's target folder using the Google Drive API via `gapi.client`, which is available on all Google Docs pages.

1. Run JavaScript in the Google Docs page context to set the API key and make the move request:
   ```javascript
   gapi.client.setApiKey('AIzaSyDrRZPb_oNAJLpNm167axWK5i85cuYG_HQ');
   gapi.client.request({
     path: '/drive/v3/files/{DOC_ID}',
     method: 'PATCH',
     params: { addParents: '{FOLDER_ID}', removeParents: 'root' }
   }).then(
     function(response) { return response.status; },
     function(error) { return error.status; }
   );
   ```
2. If the response status is 200, the move succeeded.
3. If the API returns non-200, do NOT retry. Warn the user that the doc was created successfully but remains in My Drive root. Provide both the doc URL and the target folder URL so they can move it manually.

### Step 10: Cleanup and Report

1. Kill the HTTP server:
   ```bash
   kill {PID}
   ```
   If the PID is lost, use the fallback:
   ```bash
   lsof -ti:{PORT} | xargs kill 2>/dev/null
   ```
2. Report to the user:
   - The Google Doc URL (from the browser's address bar)
   - Number of tables converted
   - Any warnings (e.g., large file size, missing H1)

---

## ERROR HANDLING

| Error | Detection | Recovery |
|---|---|---|
| Port in use | Server fails to start, "Address already in use" | Pick a new random port. Retry up to 3 times. |
| Auth required | Google Docs shows sign-in page instead of new document | Stop. Tell the user to sign into Google in Chrome, then re-run. |
| Empty paste | Screenshot shows blank document body after paste | Re-navigate to the HTML tab. Re-do Select All + Copy. Switch back to Google Doc. Cmd+A to select any partial content, then Cmd+V to paste again. Retry once. |
| Clipboard has wrong content | Pasted content is from a different document | Navigate back to the HTML tab. Click body. Cmd+A, Cmd+C. Return to Google Doc. Cmd+Z to undo the bad paste. Cmd+V to paste correct content. |
| Server PID lost | Cannot kill server by PID | Use `lsof -ti:{PORT} \| xargs kill` as fallback. |
| Very large file | HTML output > 500KB | Warn the user that paste may be slow or incomplete. Proceed anyway. |
| Converter script fails | Non-zero exit code from python3 | Report the error output. Check that the markdown file is valid UTF-8. |
| Move to folder fails | Drive API returns non-200 or token extraction fails | Do not retry. Warn the user the doc was created in My Drive root. Provide the doc URL and target folder URL for manual move. |

## EDGE CASES

- **Multiple Google accounts**: The `/u/0/` path component in Drive URLs is handled by the folder ID regex. The doc creation URL doesn't need it.
- **No H1 in markdown**: Falls back to filename stem for title. Not an error.
- **Markdown with no tables**: The converter still produces valid HTML. Headings, lists, paragraphs, and inline formatting all transfer correctly.
- **Markdown with only pipe tables**: Works. The converter handles both ASCII code-block tables and standard pipe tables.
- **Special characters in title**: Type the title directly. Google Docs handles special characters natively.
- **Shared Drive folders**: The folder ID extraction works the same way. The Drive API move step handles shared drive folders.

## USAGE

Invoke this skill by:
- `/md-to-gdoc /path/to/file.md https://drive.google.com/drive/folders/abc123`
- `/md-to-gdoc /path/to/file.md https://drive.google.com/drive/folders/abc123 "Custom Title"`
- "Convert this markdown to a Google Doc in [folder URL]"
- "Make a Google Doc from [file] in my Drive folder"
