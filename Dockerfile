# Generic placeholder Dockerfile.
# Replace with the runtime-specific build for the generated project.
FROM alpine:3.24@sha256:be2656061b536c1883c4034790e21d0a09c5aaaf51968b89368a3c0371ea2c9a

WORKDIR /app

CMD ["sh", "-c", "echo 'Replace Dockerfile with your project runtime image and command.'"]
