# AI Integration Guide for Latest News

## Overview
Your campus newsletter now has complete AI integration that fetches summaries from your backend `/process_email` endpoint and displays them in the Latest News section.

## How It Works

### 1. **Automatic Loading**
- AI summaries load automatically 2 seconds after page load
- Manual refresh available via the "🔄 Refresh AI Summaries" button

### 2. **API Integration**
The system calls your `/process_email` endpoint with this structure:
```json
{
  "subject": "Innovation Challenge 2025",
  "body": "Students are invited to participate in the annual Innovation Challenge...",
  "priority": "normal",
  "attachment": ""
}
```

### 3. **Response Handling**
Expected API response format:
```json
{
  "subject": "Innovation Challenge 2025",
  "summary": "Students are invited to participate in Innovation Challenge with $50,000 prize pool.",
  "priority": "normal",
  "attachment": ""
}
```

## Customization Options

### 1. **Change API Endpoint**
In the `loadAISummaries()` function, modify:
```javascript
const response = await fetch('/your-custom-endpoint', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        // Your custom payload
    })
});
```

### 2. **Add Multiple News Sources**
To fetch from multiple sources:
```javascript
async function loadMultipleAISummaries() {
    const sources = [
        '/process_email',
        '/campus_announcements',
        '/academic_updates'
    ];
    
    for (const endpoint of sources) {
        try {
            const response = await fetch(endpoint, { /* config */ });
            const data = await response.json();
            // Process each source
        } catch (error) {
            console.error(`Error loading from ${endpoint}:`, error);
        }
    }
}
```

### 3. **Customize Priority Levels**
Add more priority levels in the CSS:
```css
.priority-critical {
    background: linear-gradient(135deg, #7c2d12, #991b1b);
    color: white;
}
```

And update the `getEmojiForPriority()` function:
```javascript
function getEmojiForPriority(priority) {
    const emojiMap = {
        'critical': '🚨',
        'high': '🔥',
        'urgent': '⚡',
        'normal': '📰',
        'low': '📄'
    };
    return emojiMap[priority] || '📰';
}
```

### 4. **Add Real-time Updates**
For live updates, add WebSocket or periodic refresh:
```javascript
// Auto-refresh every 5 minutes
setInterval(loadAISummaries, 5 * 60 * 1000);

// Or use WebSocket for real-time updates
const socket = new WebSocket('ws://your-websocket-endpoint');
socket.onmessage = function(event) {
    const newSummary = JSON.parse(event.data);
    addSingleNewsArticle(newSummary);
};
```

## Features Included

### ✅ **Visual Indicators**
- 🤖 AI Generated badges
- Priority level indicators (HIGH, URGENT, NORMAL, LOW)
- Different border colors for AI vs manual content
- Glowing animations for AI badges

### ✅ **Loading States**
- Animated spinner during API calls
- Disabled refresh button while loading
- Error messages with auto-hide

### ✅ **Dark Mode Support**
- All new elements support your existing dark mode
- Consistent styling with your theme variables

### ✅ **Error Handling**
- Graceful fallback to default content if API fails
- User-friendly error messages
- Retry mechanism via refresh button

## Backend Requirements

Your backend should:
1. Accept POST requests to `/process_email`
2. Return JSON with `subject`, `summary`, and `priority` fields
3. Handle CORS if frontend and backend are on different domains
4. Include appropriate error responses (404, 500, etc.)

## Testing

1. **Test with your actual API**: Replace the sample data in `loadAISummaries()`
2. **Test error handling**: Temporarily break the API URL to see error states
3. **Test dark mode**: Toggle dark mode to ensure all styles work
4. **Test loading states**: Add delays to see loading animations

## Future Enhancements

Consider adding:
- 📊 Analytics for most popular news
- 🔍 Search functionality for AI summaries
- 📱 Push notifications for urgent news
- 🏷️ Category tags and filtering
- 📅 Date range filtering
- 💬 Comments or reactions