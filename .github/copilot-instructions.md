# Copilot Instructions

Project-specific instructions for working with Copilot in this workspace.

## Project Overview

**Street Light Fault Detection & Road Accident Alert System**
- Full-stack application (Python backend + React frontend)
- Real-time accident and fault detection using computer vision
- WebSocket-based communication
- SQLite database for user management and alerts

## Code Style & Conventions

### Python
- Use type hints for function parameters and return values
- Follow PEP 8 style guide
- Add docstrings to all functions
- Use meaningful variable names
- Handle exceptions explicitly

### JavaScript/React
- Use functional components with hooks (not class components)
- Use arrow functions
- Implement proper error boundaries
- Validate props and state
- Use meaningful component names

## Architecture Guidelines

### Backend (Python)
- Keep WebSocket handlers focused and modular
- Use async/await for asynchronous operations
- Validate all inputs
- Log important events
- Separate concerns (database, WebSocket, logic)

### Frontend (React)
- Use environment variables for configuration (REACT_APP_*)
- Implement proper error handling
- Use localStorage for non-sensitive data
- Lazy load components when appropriate
- Keep components small and composable

## Database

- Users table: id, email, phone, password, created_at
- Alerts table: id, user_id, alert_type, description, timestamp
- All queries use parameterized statements to prevent SQL injection

## API Endpoints (WebSocket)

Key endpoints:
- `login`: User authentication
- `register`: New user registration
- `forgot_password`: Password reset
- `log_alert`: Log detection alerts
- `get_alerts`: Retrieve user alerts

## Development Workflow

1. **Make changes** to source files
2. **Test locally** before committing
3. **Validate all inputs** in both frontend and backend
4. **Use environment variables** for configuration
5. **Add proper error handling** for all operations

## Important Files

- [README.md](/README.md) - Project overview and quick start
- [SETUP_GUIDE.md](/SETUP_GUIDE.md) - Detailed setup instructions
- [backend/ws_server.py](/backend/ws_server.py) - WebSocket server
- [backend/database.py](/backend/database.py) - Database initialization
- [frontend/src/App.jsx](/frontend/src/App.jsx) - React router setup

## Common Tasks

### Adding New API Endpoint
1. Add handler in `ws_server.py` with proper validation
2. Add corresponding error handling
3. Log the operation
4. Update client component to call new endpoint

### Adding New Database Field
1. Update schema in `database.py`
2. Create migration (or drop/recreate table for development)
3. Update corresponding handlers
4. Update UI components if needed

### Adding New Component
1. Create new JSX file in `frontend/src/`
2. Use environment variables for API URLs
3. Add to router in `App.jsx`
4. Implement proper error handling and loading states

## Performance Considerations

- Minimize re-renders in React components
- Use memoization for expensive computations
- Implement proper database indexing
- Cache frequently accessed data
- Use lazy loading for images and components

## Security Best Practices

- ✅ Passwords hashed with bcrypt
- ✅ SQL parameterized queries
- ✅ Input validation on all endpoints
- ✅ HTTPS recommended for production
- ✅ Implement rate limiting
- ✅ Add CORS configuration for production
- ✅ Secure WebSocket (WSS) for production

## Testing

Current status: Manual testing
Future: Add unit tests, integration tests

## Deployment Checklist

- [ ] Update .env files for production
- [ ] Use HTTPS/WSS for production
- [ ] Implement email/SMS notifications
- [ ] Set up monitoring and logging
- [ ] Implement database backups
- [ ] Scale backend for multiple clients
- [ ] Add rate limiting
- [ ] Implement authentication tokens

## What Not To Do

- ❌ Hard-code configuration values (use .env)
- ❌ Skip input validation
- ❌ Ignore error handling
- ❌ Use var in JavaScript
- ❌ Store sensitive data in localStorage
- ❌ Make SQL queries without parameterization
- ❌ Commit .env files to git

## References

- [README](../README.md)
- [SETUP_GUIDE](../SETUP_GUIDE.md)
- [Python async/await](https://docs.python.org/3/library/asyncio.html)
- [React Hooks](https://react.dev/reference/react/hooks)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
