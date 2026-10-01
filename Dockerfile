# Generic placeholder Dockerfile.
# Replace with the runtime-specific build for the generated project.
FROM alpine:3.24@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6

WORKDIR /app

CMD ["sh", "-c", "echo 'Replace Dockerfile with your project runtime image and command.'"]
