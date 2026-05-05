# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy the Go modules manifests
COPY go.mod ./

# Build the application
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o logistics-app main.go

# Final minimal image
FROM alpine:3.18

WORKDIR /app

# Copy the binary from the builder stage
COPY --from=builder /app/logistics-app .

# Expose port
EXPOSE 8080

# Command to run the executable
CMD ["./logistics-app"]
