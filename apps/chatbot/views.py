import uuid

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render

from .models import Conversation, Message
from .services import stream_llm


def chat(request):
    return render(request, "chatbot/chat.html")


def send_message(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request"},
            status=400
        )

    message = request.POST.get("message")

    if not message:
        return JsonResponse(
            {"error": "Message is required"},
            status=400
        )

    # --------------------------------------------------------
    # GET OR CREATE CHAT SESSION
    # --------------------------------------------------------

    session_id = request.session.get("chat_session")

    if not session_id:
        session_id = str(uuid.uuid4())

        request.session["chat_session"] = session_id

    conversation, _ = Conversation.objects.get_or_create(
        session_id=session_id
    )

    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    Message.objects.create(
        conversation=conversation,
        role="user",
        content=message,
    )

    # --------------------------------------------------------
    # GET CONVERSATION HISTORY
    # --------------------------------------------------------

    previous_messages = conversation.messages.order_by(
        "created_at"
    )

    messages = []

    for msg in previous_messages:

        messages.append(
            {
                "role": msg.role,
                "content": msg.content,
            }
        )

    # --------------------------------------------------------
    # STREAM GEMINI RESPONSE
    # --------------------------------------------------------

    def generate_response():

        full_response = ""

        for chunk in stream_llm(messages):

            # chunk is now guaranteed to be a string
            full_response += chunk

            # Send chunk to browser
            yield chunk

        # ----------------------------------------------------
        # SAVE COMPLETE AI RESPONSE
        # ----------------------------------------------------

        Message.objects.create(
            conversation=conversation,
            role="assistant",
            content=full_response,
        )

    # --------------------------------------------------------
    # RETURN STREAMING RESPONSE
    # --------------------------------------------------------

    return StreamingHttpResponse(
        generate_response(),
        content_type="text/plain",
    )