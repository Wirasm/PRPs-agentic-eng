# CLAUDE.md

This file provides comprehensive guidance for working with Go applications.

## Core Development Philosophy

### Simplicity & Clarity
Go values simplicity and readability. Write clear, idiomatic Go code that others can easily understand and maintain.

### Explicit Over Implicit
Go prefers explicit error handling and clear interfaces. Avoid magic and hidden behavior in favor of explicit, readable code.

### Concurrency by Design
Go's goroutines and channels make concurrent programming accessible. Use them to build efficient, concurrent applications.

## Core Principles

### Composition Over Inheritance
- **Embed Structs**: Use struct embedding for composition
- **Interfaces**: Design small, focused interfaces
- **Duck Typing**: If it walks like a duck and quacks like a duck, it's a duck

### Error Handling
- **Explicit Errors**: Always check and handle errors explicitly
- **Error Wrapping**: Use fmt.Errorf with %w to wrap errors
- **Custom Errors**: Implement error interface for domain-specific errors

### Concurrency
- **Goroutines**: Lightweight threads for concurrent execution
- **Channels**: Communication between goroutines
- **Select**: Non-blocking channel operations

## 🤖 AI Assistant Guidelines

### Context Awareness
- When implementing features, always check existing patterns first
- Use existing error types and patterns in the codebase
- Check for similar functionality in other packages
- Follow existing naming conventions and package organization

### Common Pitfalls to Avoid
- Ignoring errors (never use _ for error returns)
- Creating goroutine leaks
- Using global variables unnecessarily
- Not closing channels when done

### Workflow Patterns
- Write tests BEFORE implementation (TDD)
- Use go fmt for consistent formatting
- Run go vet for static analysis
- Use go mod tidy to clean dependencies

## 🐹 Go Best Practices

### Project Structure

```
cmd/
├── myapp/
│   └── main.go           # Application entry point
internal/
├── config/               # Configuration handling
├── handlers/             # HTTP handlers
├── models/               # Data structures
├── services/             # Business logic
└── storage/              # Data access layer
pkg/
├── api/                  # Public API definitions
└── utils/                # Utility functions
go.mod
go.sum
```

### Module Configuration

```go
// go.mod
module github.com/user/myapp

go 1.21

require (
    github.com/gorilla/mux v1.8.0
    github.com/lib/pq v1.10.9
    golang.org/x/crypto v0.14.0
)
```

### Error Handling Patterns

```go
// Custom error type
type AppError struct {
    Code    string
    Message string
    Err     error
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %s (%v)", e.Code, e.Message, e.Err)
    }
    return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// Function with proper error handling
func GetUser(ctx context.Context, id int64) (*User, error) {
    const op = "GetUser"
    
    user, err := db.QueryUser(ctx, id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, &AppError{
                Code:    "USER_NOT_FOUND",
                Message: fmt.Sprintf("user with id %d not found", id),
                Err:     err,
            }
        }
        return nil, fmt.Errorf("%s: failed to query user: %w", op, err)
    }
    
    return user, nil
}
```

### HTTP Server Patterns

```go
// Handler with proper error handling
func (h *Handler) GetUserHandler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    
    vars := mux.Vars(r)
    id, err := strconv.ParseInt(vars["id"], 10, 64)
    if err != nil {
        h.respondError(w, http.StatusBadRequest, "invalid user id")
        return
    }
    
    user, err := h.service.GetUser(ctx, id)
    if err != nil {
        var appErr *AppError
        if errors.As(err, &appErr) {
            switch appErr.Code {
            case "USER_NOT_FOUND":
                h.respondError(w, http.StatusNotFound, appErr.Message)
            default:
                h.respondError(w, http.StatusInternalServerError, "internal server error")
            }
        } else {
            h.respondError(w, http.StatusInternalServerError, "internal server error")
        }
        return
    }
    
    h.respondJSON(w, http.StatusOK, user)
}

// Server setup with graceful shutdown
func StartServer(ctx context.Context, addr string, handler http.Handler) error {
    srv := &http.Server{
        Addr:         addr,
        Handler:      handler,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }
    
    go func() {
        <-ctx.Done()
        shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()
        srv.Shutdown(shutdownCtx)
    }()
    
    return srv.ListenAndServe()
}
```

### Concurrency Patterns

```go
// Worker pool pattern
func ProcessItems(ctx context.Context, items []Item) error {
    const numWorkers = 10
    
    jobs := make(chan Item, len(items))
    results := make(chan error, len(items))
    
    // Start workers
    for i := 0; i < numWorkers; i++ {
        go worker(ctx, jobs, results)
    }
    
    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)
    
    // Collect results
    var errors []error
    for i := 0; i < len(items); i++ {
        if err := <-results; err != nil {
            errors = append(errors, err)
        }
    }
    
    if len(errors) > 0 {
        return fmt.Errorf("processing failed: %v", errors)
    }
    
    return nil
}

func worker(ctx context.Context, jobs <-chan Item, results chan<- error) {
    for {
        select {
        case item, ok := <-jobs:
            if !ok {
                return
            }
            results <- processItem(ctx, item)
        case <-ctx.Done():
            return
        }
    }
}
```

### Testing Patterns

```go
func TestGetUser(t *testing.T) {
    tests := []struct {
        name    string
        userID  int64
        want    *User
        wantErr string
    }{
        {
            name:   "existing user",
            userID: 1,
            want:   &User{ID: 1, Name: "John Doe"},
        },
        {
            name:    "non-existing user",
            userID:  999,
            wantErr: "USER_NOT_FOUND",
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            ctx := context.Background()
            
            got, err := GetUser(ctx, tt.userID)
            
            if tt.wantErr != "" {
                if err == nil {
                    t.Fatalf("expected error containing %q, got nil", tt.wantErr)
                }
                if !strings.Contains(err.Error(), tt.wantErr) {
                    t.Fatalf("expected error containing %q, got %q", tt.wantErr, err.Error())
                }
                return
            }
            
            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }
            
            if !reflect.DeepEqual(got, tt.want) {
                t.Fatalf("got %+v, want %+v", got, tt.want)
            }
        })
    }
}

// Benchmark example
func BenchmarkProcessItem(b *testing.B) {
    item := Item{ID: 1, Data: "test"}
    ctx := context.Background()
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        processItem(ctx, item)
    }
}
```

## 🛠️ Development Tools

### Essential Go Commands

```bash
# Development
go run main.go                # Run program
go build                      # Build binary
go test ./...                 # Run all tests
go test -v ./...              # Verbose test output
go test -race ./...           # Test with race detection

# Code quality
go fmt ./...                  # Format code
go vet ./...                  # Static analysis
go mod tidy                   # Clean dependencies

# Documentation
go doc                        # Show documentation
godoc -http=:6060            # Local documentation server

# Profiling
go test -bench=.             # Run benchmarks
go test -cpuprofile=cpu.prof # CPU profiling
```

### Recommended Tools
- golangci-lint (comprehensive linting)
- delve (debugger)
- govulncheck (security scanning)

## 🔒 Security & Safety

### Input Validation
```go
import (
    "net/mail"
    "regexp"
    "unicode/utf8"
)

func ValidateEmail(email string) error {
    if !utf8.ValidString(email) {
        return errors.New("invalid UTF-8 in email")
    }
    
    _, err := mail.ParseAddress(email)
    if err != nil {
        return fmt.Errorf("invalid email format: %w", err)
    }
    
    return nil
}

func ValidateName(name string) error {
    if len(name) == 0 {
        return errors.New("name cannot be empty")
    }
    
    if len(name) > 100 {
        return errors.New("name too long")
    }
    
    // Only allow letters, spaces, and hyphens
    matched, _ := regexp.MatchString(`^[a-zA-Z\s\-]+$`, name)
    if !matched {
        return errors.New("name contains invalid characters")
    }
    
    return nil
}
```

### Context Usage
```go
// Always pass context as first parameter
func ProcessData(ctx context.Context, data []byte) error {
    // Check for cancellation
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }
    
    // Use context in downstream calls
    result, err := api.Process(ctx, data)
    if err != nil {
        return err
    }
    
    return nil
}

// Set timeouts appropriately
func CallExternalAPI() error {
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    
    return ProcessData(ctx, data)
}
```

## 📊 Performance Guidelines

### Memory Management
```go
// Pre-allocate slices when size is known
func ProcessItems(count int) []Result {
    results := make([]Result, 0, count)  // Pre-allocate capacity
    
    for i := 0; i < count; i++ {
        results = append(results, process(i))
    }
    
    return results
}

// Use string builder for concatenation
func BuildString(parts []string) string {
    var sb strings.Builder
    sb.Grow(estimateSize(parts))  // Pre-allocate if possible
    
    for _, part := range parts {
        sb.WriteString(part)
    }
    
    return sb.String()
}

// Pool expensive objects
var bufferPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 0, 1024)
    },
}

func ProcessWithBuffer() {
    buf := bufferPool.Get().([]byte)
    defer bufferPool.Put(buf[:0])  // Reset length, keep capacity
    
    // Use buf...
}
```

## ⚠️ Critical Guidelines

1. **Always handle errors** - Never ignore error return values
2. **Use context.Context** - Pass it as the first parameter to functions
3. **Close channels** - Always close channels when done sending
4. **Don't ignore race conditions** - Use `go test -race`
5. **Follow naming conventions** - Use camelCase, short names for small scopes
6. **Keep interfaces small** - Prefer many small interfaces over few large ones
7. **Use go fmt** - Always format your code consistently
8. **Write tests** - Test coverage should be high and meaningful
9. **Handle panics** - Use recover() only where appropriate
10. **Profile before optimizing** - Don't guess where the bottlenecks are

## 📋 Pre-commit Checklist

- [ ] All tests pass: `go test ./...`
- [ ] No race conditions: `go test -race ./...`
- [ ] Code is formatted: `go fmt ./...`
- [ ] No vet warnings: `go vet ./...`
- [ ] Dependencies are clean: `go mod tidy`
- [ ] Error handling is comprehensive
- [ ] Context is used appropriately
- [ ] Documentation is updated

## 🔧 Useful Commands

```bash
# Development workflow
go test ./... -short          # Run only short tests
go test -run TestSpecific     # Run specific test
go test -bench=BenchName      # Run specific benchmark

# Debugging
go test -v -run TestName      # Verbose test output
dlv debug                     # Start debugger

# Performance analysis
go test -bench=. -memprofile=mem.prof
go tool pprof mem.prof

# Security
govulncheck ./...             # Check for vulnerabilities
go list -m all                # List all dependencies

# Build variants
GOOS=linux go build          # Cross-compile for Linux
go build -ldflags="-s -w"     # Strip debug info for smaller binary
```

---

*Keep this guide updated as patterns evolve. Simplicity, clarity, and explicit error handling, always.*