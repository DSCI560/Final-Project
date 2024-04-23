# css = '''
# <style>
# .chat-message {
#     padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
# }
# .chat-message.user {
#     background-color: #2b313e
# }
# .chat-message.bot {
#     background-color: #475063
# }
# .chat-message .avatar {
#   width: 20%;
# }
# .chat-message .avatar img {
#   max-width: 78px;
#   max-height: 78px;
#   border-radius: 50%;
#   object-fit: cover;
# }
# .chat-message .message {
#   width: 80%;
#   padding: 0 1.5rem;
#   color: #fff;
# }
# '''


css = '''
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: #f6f6f6;
}
.chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 1rem;
    background-color: #e8f5e9;
}
.chat-message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
}
.chat-message.user {
    justify-content: flex-end;
}
.chat-message.bot {
    justify-content: flex-start;
}
.chat-message.bot .message {
    background-color: #ffffff;
    border: 2px solid #2196f3;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 1rem;
}
.chat-message .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.chat-message .message {
    background-color: #ffffff;
    color: #333333;
    padding: 0.75rem 1rem;
    border-radius: 1rem;
    max-width: 70%;
}
.chat-message.user .message {
    background-color: #4caf50;
    color: #ffffff;
}
.sidebar {
    background-color: #f8f9fa;
    padding: 1rem;
}
.sidebar-title {
    color: #1565c0;
    font-size: 1.25rem;
    font-weight: bold;
    margin-bottom: 1rem;
}
.sidebar-button {
    background-color: #2196f3;
    color: #ffffff;
    border: none;
    border-radius: 0.25rem;
    padding: 0.5rem 1rem;
    margin-top: 1rem;
    cursor: pointer;
}
.sidebar-button:hover {
    background-color: #1976d2;
}
.user-input {
    margin-top: 1rem;
}
.user-input input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
}
.user-input input:focus {
    outline: none;
    border-color: #2196f3;
    box-shadow: 0 0 0 0.2rem rgba(33, 150, 243, 0.25);
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://images.rawpixel.com/image_png_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTA4L3Jhd3BpeGVsX29mZmljZV8yOV8zZF9jaGFyYWN0ZXJfaWxsdXN0cmF0aW9uX3JvYm90X2Z1bGxfYm9keV9zdF8zN2MxNWUzNC1hODk5LTQxYTMtOThjYy1jYzEwMjhmNGVmNzIucG5n.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">    
    <div class="message">{{MSG}}</div>
</div>
'''
