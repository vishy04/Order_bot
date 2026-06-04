

## Assistant

```mermaid
sequenceDiagram
    autonumber

    participant Meta as Meta / WhatsApp Cloud API
    participant Webhook as Your Webhook Server
    participant Security as Signature Verification
    participant Queue as Async Queue / Worker
    participant App as Business Logic

    rect rgb(230, 245, 255)
        note over Meta,Webhook: Phase 1: Webhook Verification

        Meta->>Webhook: GET /webhook?hub.verify_token=YOUR_TOKEN&hub.challenge=CHALLENGE
        Webhook->>Webhook: Compare hub.verify_token with expected token

        alt Token is valid
            Webhook-->>Meta: HTTP 200 with hub.challenge
            note over Meta,Webhook: Webhook endpoint is verified
        else Token is invalid
            Webhook-->>Meta: HTTP 403 Forbidden
            note over Meta,Webhook: Verification fails
        end
    end

    rect rgb(235, 255, 235)
        note over Meta,Webhook: Phase 2: Event Reception

        Meta->>Webhook: POST /webhook with JSON payload
        note right of Meta: Payload path:<br/>entry[].changes[].value.messages[]

        Meta->>Webhook: Header: X-Hub-Signature-256
        Webhook->>Security: Verify signature using app secret
        Security->>Security: hmac + hashlib SHA-256 comparison

        alt Signature is valid
            Security-->>Webhook: Request is trusted
            Webhook->>Webhook: Extract message fields
            note right of Webhook: from<br/>type<br/>content

            alt Message type is text
                Webhook->>Webhook: Read text.body
            else Message type is image
                Webhook->>Webhook: Read image.id
                Webhook->>Meta: Download media using image.id
                Meta-->>Webhook: Media file / URL
            else Message type is document
                Webhook->>Webhook: Read document.id / filename
            else Message type is interactive
                Webhook->>Webhook: Read button/list reply
            else Message type is location
                Webhook->>Webhook: Read latitude and longitude
            end

            Webhook->>Queue: Push event for async processing
            Webhook-->>Meta: HTTP 200 immediately

            note over Webhook,Meta: Golden rule: respond fast, ideally immediately

            Queue->>App: Process message in background
            App->>App: Run business logic
            App->>Meta: Optionally send reply message

        else Signature is invalid
            Security-->>Webhook: Request is not trusted
            Webhook-->>Meta: HTTP 403 Forbidden
        end
    end

    rect rgb(255, 245, 230)
        note over Meta,Webhook: Timeout and Retry Behavior

        alt Webhook responds within 20 seconds
            Meta->>Meta: Event marked as delivered
        else Webhook takes too long
            Meta->>Webhook: Retry same notification
            note over Webhook,App: Can cause duplicate messages and state bugs
        end
    end
```

## User

can you give little more simpler diagram for begineer

## Assistant

```mermaid
flowchart TD
    A[Customer sends a WhatsApp message] --> B[Meta receives the message]
    B --> C[Meta sends POST request to your webhook]

    C --> D[Your FastAPI or Flask webhook endpoint]

    D --> E{Is request really from Meta?}

    E -->|No| F[Reject request<br>Return HTTP 403]

    E -->|Yes| G[Read message data]

    G --> H[Get sender number]
    G --> I[Get message type]
    G --> J[Get message content]

    I --> K{Message type}

    K -->|Text| L[Read text body]
    K -->|Image| M[Get image ID<br>Download image later]
    K -->|Document| N[Get document ID]
    K -->|Location| O[Get latitude and longitude]
    K -->|Button/List| P[Read selected option]

    L --> Q[Put message into background task]
    M --> Q
    N --> Q
    O --> Q
    P --> Q

    Q --> R[Return HTTP 200 immediately to Meta]

    R --> S[Process message in background]
    S --> T[Optional: send reply to customer]

    R --> U[Meta knows webhook worked]

    D -. First time setup .-> V[Meta sends GET verification request]
    V --> W[Check verify token]
    W --> X[Return challenge code]
    X --> Y[Webhook is verified]
```

A very simple mental model:

```mermaid
flowchart LR
    A[WhatsApp User] --> B[Meta]
    B --> C[Your Webhook URL]
    C --> D[Check Security]
    D --> E[Read Message]
    E --> F[Return 200 Fast]
    F --> G[Process Later]
    G --> H[Send Reply if needed]
```

Key idea:

```text
Meta sends events to your webhook.
Your webhook checks the request, reads the message, returns 200 quickly,
then processes the message in the background.
```
