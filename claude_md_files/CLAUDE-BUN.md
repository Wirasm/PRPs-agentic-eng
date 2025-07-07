# CLAUDE.md

This file provides comprehensive guidance for working with Bun applications.

## Core Development Philosophy

### Speed & Simplicity
Bun is designed for speed - both in development and runtime. Leverage Bun's native APIs and built-in tools for optimal performance.

### TypeScript First
Bun natively supports TypeScript without transpilation. Embrace strong typing and modern JavaScript/TypeScript features.

### Node.js Compatibility
While Bun aims for Node.js compatibility, prefer Bun's native APIs when available for better performance.

## Core Principles

### Native Performance
- **Use Bun APIs**: Prefer Bun.serve over Express for HTTP servers
- **Built-in SQLite**: Use Bun's native SQLite database when possible
- **Native Fetch**: Leverage Bun's optimized fetch implementation

### TypeScript Integration
- **No Build Step**: Run TypeScript files directly with Bun
- **Strict Types**: Use TypeScript's strict mode for better code quality
- **Modern Syntax**: Use latest ES features supported by Bun

### Development Speed
- **Hot Reload**: Use `--hot` flag for instant reloads
- **Fast Package Manager**: Use Bun's package manager over npm
- **Built-in Test Runner**: Use `bun test` for testing

## 🤖 AI Assistant Guidelines

### Context Awareness
- When implementing features, check for Bun-specific APIs first
- Use existing TypeScript patterns in the codebase
- Check for similar functionality in other modules
- Follow existing project structure and naming conventions

### Common Pitfalls to Avoid
- Mixing Node.js APIs with Bun APIs unnecessarily
- Ignoring TypeScript errors
- Using outdated JavaScript patterns
- Not leveraging Bun's performance features

### Workflow Patterns
- Write TypeScript with strict types
- Use Bun's native testing framework
- Leverage hot reload for development
- Profile with Bun's built-in tools

## 🧅 Bun Best Practices

### Project Structure

```
src/
├── index.ts              # Main entry point
├── server.ts             # HTTP server setup
├── config/
│   └── env.ts            # Environment configuration
├── handlers/
│   └── api.ts            # API route handlers
├── models/
│   └── types.ts          # TypeScript types
├── services/
│   └── business.ts       # Business logic
├── utils/
│   └── helpers.ts        # Utility functions
└── db/
    └── schema.ts         # Database schema
package.json
tsconfig.json
bun.lockb
```

### Package Configuration

```json
{
  "name": "my-bun-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "bun --hot src/index.ts",
    "start": "bun src/index.ts",
    "test": "bun test",
    "build": "bun build src/index.ts --outdir ./dist --target bun",
    "typecheck": "tsc --noEmit",
    "lint": "eslint src/"
  },
  "dependencies": {
    "bun-types": "latest"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "skipLibCheck": true,
    "types": ["bun-types"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### HTTP Server with Bun.serve

```typescript
// server.ts
import type { Server } from "bun";

interface APIResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
}

class APIServer {
  private server: Server | null = null;

  async start(port: number = 3000): Promise<void> {
    this.server = Bun.serve({
      port,
      async fetch(req: Request): Promise<Response> {
        const url = new URL(req.url);
        
        // CORS headers
        const headers = {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization",
        };

        if (req.method === "OPTIONS") {
          return new Response(null, { status: 200, headers });
        }

        try {
          const response = await handleRoute(url.pathname, req);
          return new Response(JSON.stringify(response), {
            headers: { ...headers, "Content-Type": "application/json" },
            status: response.success ? 200 : 400,
          });
        } catch (error) {
          console.error("Server error:", error);
          const errorResponse: APIResponse = {
            success: false,
            error: "Internal server error",
          };
          return new Response(JSON.stringify(errorResponse), {
            headers: { ...headers, "Content-Type": "application/json" },
            status: 500,
          });
        }
      },
    });

    console.log(`Server running on http://localhost:${port}`);
  }

  async stop(): Promise<void> {
    if (this.server) {
      this.server.stop();
      this.server = null;
    }
  }
}

async function handleRoute(pathname: string, req: Request): Promise<APIResponse> {
  switch (pathname) {
    case "/api/users":
      return handleUsers(req);
    case "/api/health":
      return { success: true, data: { status: "ok", timestamp: Date.now() } };
    default:
      return { success: false, error: "Route not found" };
  }
}

async function handleUsers(req: Request): Promise<APIResponse> {
  if (req.method === "GET") {
    // Fetch users logic
    return { success: true, data: [] };
  }
  
  if (req.method === "POST") {
    const body = await req.json();
    // Create user logic
    return { success: true, data: body };
  }
  
  return { success: false, error: "Method not allowed" };
}
```

### Database with Native SQLite

```typescript
// db/database.ts
import { Database } from "bun:sqlite";

export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

export class UserDB {
  private db: Database;

  constructor(path: string = "app.sqlite") {
    this.db = new Database(path);
    this.init();
  }

  private init(): void {
    // Create tables
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
  }

  async createUser(email: string, name: string): Promise<User> {
    const stmt = this.db.prepare(`
      INSERT INTO users (email, name) 
      VALUES (?, ?) 
      RETURNING *
    `);
    
    const result = stmt.get(email, name) as User;
    return result;
  }

  async getUserById(id: number): Promise<User | null> {
    const stmt = this.db.prepare("SELECT * FROM users WHERE id = ?");
    const result = stmt.get(id) as User | undefined;
    return result || null;
  }

  async getAllUsers(): Promise<User[]> {
    const stmt = this.db.prepare("SELECT * FROM users ORDER BY created_at DESC");
    return stmt.all() as User[];
  }

  async updateUser(id: number, updates: Partial<Omit<User, 'id' | 'created_at'>>): Promise<User | null> {
    const fields = Object.keys(updates);
    const values = Object.values(updates);
    
    if (fields.length === 0) {
      return this.getUserById(id);
    }
    
    const setClause = fields.map(field => `${field} = ?`).join(", ");
    const stmt = this.db.prepare(`
      UPDATE users 
      SET ${setClause} 
      WHERE id = ? 
      RETURNING *
    `);
    
    const result = stmt.get(...values, id) as User | undefined;
    return result || null;
  }

  close(): void {
    this.db.close();
  }
}
```

### Environment Configuration

```typescript
// config/env.ts
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().default("app.sqlite"),
  JWT_SECRET: z.string().min(32),
  API_TIMEOUT: z.coerce.number().default(30000),
});

function loadEnv() {
  const env = {
    NODE_ENV: Bun.env.NODE_ENV,
    PORT: Bun.env.PORT,
    DATABASE_URL: Bun.env.DATABASE_URL,
    JWT_SECRET: Bun.env.JWT_SECRET,
    API_TIMEOUT: Bun.env.API_TIMEOUT,
  };

  try {
    return envSchema.parse(env);
  } catch (error) {
    console.error("Invalid environment configuration:", error);
    process.exit(1);
  }
}

export const config = loadEnv();
export type Config = typeof config;
```

### Testing with Bun Test

```typescript
// __tests__/user.test.ts
import { describe, it, expect, beforeEach, afterEach } from "bun:test";
import { UserDB } from "../src/db/database";

describe("UserDB", () => {
  let db: UserDB;

  beforeEach(() => {
    db = new UserDB(":memory:"); // Use in-memory database for tests
  });

  afterEach(() => {
    db.close();
  });

  it("should create a user", async () => {
    const user = await db.createUser("test@example.com", "Test User");
    
    expect(user.email).toBe("test@example.com");
    expect(user.name).toBe("Test User");
    expect(user.id).toBeGreaterThan(0);
  });

  it("should get user by id", async () => {
    const created = await db.createUser("test@example.com", "Test User");
    const found = await db.getUserById(created.id);
    
    expect(found).toEqual(created);
  });

  it("should return null for non-existent user", async () => {
    const found = await db.getUserById(999);
    expect(found).toBeNull();
  });

  it("should update user", async () => {
    const created = await db.createUser("test@example.com", "Test User");
    const updated = await db.updateUser(created.id, { name: "Updated Name" });
    
    expect(updated?.name).toBe("Updated Name");
    expect(updated?.email).toBe("test@example.com");
  });
});
```

## 🛠️ Development Tools

### Essential Bun Commands

```bash
# Development
bun run dev                   # Start with hot reload
bun run start                 # Start production
bun test                      # Run tests
bun test --watch              # Watch mode testing

# Package management
bun install                   # Install dependencies
bun add <package>             # Add dependency
bun remove <package>          # Remove dependency
bun update                    # Update dependencies

# Build and bundle
bun build src/index.ts        # Bundle for production
bun run typecheck             # TypeScript checking

# Utilities
bun --version                 # Check Bun version
bun upgrade                   # Upgrade Bun
```

### Recommended Extensions
- TypeScript and Bun support in your editor
- ESLint for code quality
- Prettier for formatting

## 🔒 Security & Performance

### Input Validation with Zod

```typescript
import { z } from "zod";

export const CreateUserSchema = z.object({
  email: z.string().email("Invalid email format"),
  name: z.string().min(2, "Name must be at least 2 characters").max(50, "Name too long"),
  age: z.number().int().min(18, "Must be at least 18").max(120, "Invalid age"),
});

export type CreateUserInput = z.infer<typeof CreateUserSchema>;

export function validateCreateUser(data: unknown): CreateUserInput {
  return CreateUserSchema.parse(data);
}

// Usage in handler
async function createUser(req: Request): Promise<APIResponse> {
  try {
    const body = await req.json();
    const validatedData = validateCreateUser(body);
    
    // Create user with validated data
    const user = await db.createUser(validatedData.email, validatedData.name);
    return { success: true, data: user };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { 
        success: false, 
        error: `Validation error: ${error.errors.map(e => e.message).join(", ")}` 
      };
    }
    throw error;
  }
}
```

### Performance Optimization

```typescript
// Use Bun's native fetch for better performance
async function fetchData(url: string): Promise<any> {
  const response = await fetch(url, {
    headers: {
      "User-Agent": "MyApp/1.0",
    },
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}

// Stream large responses
async function streamLargeData(): Promise<Response> {
  const stream = new ReadableStream({
    start(controller) {
      // Generate data chunks
      for (let i = 0; i < 1000; i++) {
        controller.enqueue(`data chunk ${i}\n`);
      }
      controller.close();
    },
  });
  
  return new Response(stream, {
    headers: {
      "Content-Type": "text/plain",
      "Transfer-Encoding": "chunked",
    },
  });
}
```

## ⚠️ Critical Guidelines

1. **Use TypeScript strictly** - Enable all strict compiler options
2. **Prefer Bun APIs** - Use native Bun features over Node.js when available
3. **Validate all inputs** - Use Zod or similar for runtime validation
4. **Handle errors properly** - Don't let unhandled promises crash the app
5. **Use environment variables** - Never hardcode secrets or config
6. **Test thoroughly** - Use Bun's fast test runner extensively
7. **Hot reload in development** - Use `--hot` flag for faster development
8. **Profile performance** - Use Bun's built-in profiling tools
9. **Keep dependencies minimal** - Leverage Bun's built-in features
10. **Use modern JavaScript** - Take advantage of latest ES features

## 📋 Pre-commit Checklist

- [ ] All tests pass: `bun test`
- [ ] No TypeScript errors: `bun run typecheck`
- [ ] Code is linted: `bun run lint`
- [ ] Environment variables are documented
- [ ] Error handling is comprehensive
- [ ] Performance impact considered
- [ ] Security best practices followed

## 🔧 Useful Commands

```bash
# Development workflow
bun --hot src/index.ts        # Hot reload development
bun test --coverage           # Test with coverage
bun run build                 # Production build

# Debugging
bun --inspect src/index.ts    # Enable inspector
bun --prof src/index.ts       # CPU profiling

# Package management
bun install --frozen-lockfile # Install exact versions
bun outdated                  # Check for updates
bun why <package>             # Why is package installed

# Performance
bun build --minify            # Minified build
bun --smol src/index.ts       # Memory-optimized mode
```

---

*Keep this guide updated as Bun evolves. Speed, simplicity, and TypeScript-first development, always.*