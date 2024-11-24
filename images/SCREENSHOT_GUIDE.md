# Screenshot Guide for README

This guide will help you capture the right screenshots to showcase your Multi-Agent Code Assistant.

## 📸 Required Screenshots

### 1. `chat-interface.png`
**What to capture:**
- Main chat interface with a few messages
- Show the clean, modern UI design
- Include both user and assistant messages
- Make sure the sidebar and header are visible

**How to take it:**
1. Open the app at http://localhost:3000
2. Have a conversation like: "Create a REST API with FastAPI"
3. Capture the full browser window
4. Recommended size: 1920x1080 or 1440x900

---

### 2. `agent-trace.png`
**What to capture:**
- A message with the Agent Execution Trace visible
- Show multiple agents (Planner, Coder, Reviewer, etc.)
- Make sure the execution time is visible

**How to take it:**
1. Click "Show Agent Trace" in the sidebar
2. Send a complex query like: "Build a user authentication system with JWT"
3. Wait for the response with agent trace
4. Capture the agent trace section expanded
5. Highlight the multi-agent collaboration

---

### 3. `code-generation.png`
**What to capture:**
- An assistant message with generated code
- Show syntax highlighting
- Include both the question and the code response
- Make the code readable

**How to take it:**
1. Ask: "Write a Python function to calculate Fibonacci numbers"
2. Wait for the code response
3. Capture the message with the code block
4. Ensure syntax highlighting is visible

---

### 4. `debugging-example.png`
**What to capture:**
- A debugging scenario
- Show problem identification and solution
- Include the debugger agent in action (if trace is visible)

**How to take it:**
1. Ask: "Debug this code: [paste some buggy code]"
2. Or: "Why isn't my React component re-rendering?"
3. Capture the assistant's analysis and solution
4. Show the step-by-step debugging process

---

### 5. `chat-history.png`
**What to capture:**
- Sidebar with multiple chat sessions
- Show the "New Chat" button
- Display several conversation titles with dates
- Highlight the chat management features

**How to take it:**
1. Create 3-4 different chat sessions with different topics
2. Make sure the sidebar is expanded
3. Capture the left side showing the chat history
4. Show the active chat highlighted

---

## 🎨 Tips for Great Screenshots

### General Guidelines:
- ✅ Use **full browser window** captures
- ✅ **Clean up**: Close unnecessary tabs/windows
- ✅ **Dark mode** looks more professional
- ✅ Use **real, meaningful content** (not "test test test")
- ✅ Crop to remove desktop taskbar/menu bar
- ✅ Ensure **high resolution** (at least 1280px width)

### Recommended Tools:
- **Windows**: Snipping Tool (Win + Shift + S)
- **Windows**: Greenshot (free download)
- **Browser DevTools**: F12 > Device toolbar for consistent sizing

### Image Optimization:
After taking screenshots:
1. Save as PNG (better quality than JPG for UI)
2. Optionally compress with TinyPNG or similar
3. Rename exactly as listed above
4. Place in the `images/` folder

---

## 📝 Sample Conversation Topics

Use these to generate good-looking screenshots:

1. **Simple Code Generation:**
   - "Create a FastAPI endpoint for user registration"
   - "Write a Python function to reverse a linked list"
   - "Build a React component for a todo list"

2. **Complex Tasks (shows agent collaboration):**
   - "Build a complete authentication system with JWT tokens"
   - "Create a REST API with CRUD operations and database"
   - "Design and implement a caching layer for my API"

3. **Debugging:**
   - "Why is my React component not re-rendering?"
   - "Debug this SQL query that's running slow"
   - "Find the memory leak in this Python code"

4. **Optimization:**
   - "Optimize this database query for better performance"
   - "Refactor this code to follow SOLID principles"
   - "Improve the time complexity of this algorithm"

---

## ✅ Checklist Before Committing

- [ ] All 5 screenshots are captured
- [ ] Images are in PNG format
- [ ] Images are properly named (exactly as in README.md)
- [ ] Images are saved in `images/` folder
- [ ] Screenshots show real, meaningful content
- [ ] UI looks clean and professional
- [ ] Text is readable in all screenshots
- [ ] No sensitive information visible

---

## 🚀 After Adding Screenshots

Once you've added all screenshots:

```bash
cd C:\Users\nghia\Desktop\LLMs\multi-agent-code-assistant
git add images/
git add README.md
git commit -m "Add UI screenshots showcasing key features"
git push origin main
```

Then check your README on GitHub to see how it looks!
