# Chat Application

This is a simple **messenger** app built with **Django REST Framework**.  
It includes the following functionality:
- Chats (`direct`, `group`, `channel`)
- Participants with roles (`admin`, `moderator`, `member`, `subscriber`)
- Invitations (`pending`, `accepted`, `rejected`)  
- Messages, with denormalized `last_message` in each chat  
- Blocking and unblocking participants

## Features

1. **Chat**:
   - `GET /api/chats/`: list user chats (accepted or pending)
   - `POST /api/chats/`: create a new chat (direct, group, or channel)

2. **Chat detail**:
   - `GET /api/chats/<chat_id>/`: retrieve detail
   - `PATCH/PUT /api/chats/<chat_id>/`: update (only admin)
   - `DELETE /api/chats/<chat_id>/`: delete (only admin)

3. **Messages**:
   - `GET /api/chats/<chat_id>/messages/`
   - `POST /api/chats/<chat_id>/messages/` (denormalizes last_message)
   - `GET/PATCH/PUT/DELETE /api/chats/<chat_id>/messages/<message_id>/`
     - remove last message => re-calculate new last_message

4. **Invitations**:
   - `POST /api/chats/<chat_id>/invite/`: invite user => participant with `pending`
   - `POST /api/chats/<chat_id>/invite/accept/`: user changes status => `accepted`
   - `POST /api/chats/<chat_id>/invite/reject/`: user changes status => `rejected`

5. **Leaving a chat**:
   - `POST /api/chats/<chat_id>/leave/` (only for group/channel)

6. **Blocking**:
   - `POST /api/chats/<chat_id>/block/`: block user
   - `POST /api/chats/<chat_id>/unblock/`: unblock user

