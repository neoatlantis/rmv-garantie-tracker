#!/usr/bin/env python3

from email import message_from_file
import os

def pullout (m):
    """Extracts content from an e-mail message.
    This works for multipart and nested multipart messages too.
    m   -- email.Message() or mailbox.Message()
    key -- Initial message ID (some string)
    Returns tuple(Text, Html, Files, Parts)
    Text  -- All text from all parts.
    Html  -- All HTMLs from all parts
    Files -- Dictionary mapping extracted file to message ID it belongs to.
    Parts -- Number of parts in original message.
    """
    Html = b""
    Text = b""
    if not m.is_multipart():
        # Not an attachment!
        # See where this belongs. Text, Html or some other data:
        cp = m.get_content_type()
        if cp=="text/plain":
            Text += m.get_payload(decode=True)
        elif cp=="text/html":
            Html += m.get_payload(decode=True)
        return Text, Html
    # This IS a multipart message.
    # So, we iterate over it and call pullout() recursively for each part.
    y = 0
    while 1:
        # If we cannot get the payload, it means we hit the end:
        try:
            pl = m.get_payload(y)
        except:
            break
        # pl is a new Message object which goes back to pullout
        t, h = pullout(pl)
        Text += t
        Html += h
        y += 1
    return Text, Html
