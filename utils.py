def trim_history(messages):
    """Trim the conversation history to stay within token limits.
    Keeps the system prompt(s) and the most recent user/assistant messages.
    """
    max_tokens = 3000  # Adjust according to your model's context window

    # Try to use tiktoken for accurate token counting; fallback to word count
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        def count_tokens(msg):
            # Count tokens in the message content
            return len(enc.encode(msg.get('content', '')))
    except Exception:
        def count_tokens(msg):
            # Rough approximation: one token per word
            return len(msg.get('content', '').split())

    # Preserve all system messages (they are usually essential)
    system_msgs = [msg for msg in messages if msg.get('role') == 'system']
    # Work backwards through non‑system messages, adding until limit is hit
    kept = []
    total = sum(count_tokens(m) for m in system_msgs)
    for msg in reversed(messages):
        if msg.get('role') == 'system':
            continue
        msg_tokens = count_tokens(msg)
        if total + msg_tokens > max_tokens:
            break
        total += msg_tokens
        kept.insert(0, msg)  # prepend to keep original order

    # Combine system messages (at the start) with the kept recent messages
    return system_msgs + kept