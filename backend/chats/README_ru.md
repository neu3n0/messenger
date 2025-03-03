# Желаемый функционал

- CHAT'S API:
  - Создание чата: /api/chats/ (POST)
  - Получение списка чатов: /api/chats/ (GET)
  - Получение информации о чате: /api/chats/<int:pk>/ (GET)
  - Обновлении инофрмации о чате: /api/chats/<int:pk>/ (PATCH/PUT)
  - Удаление чата: /api/chats/<int:pk>/ (DELETE)
  - Приглашение человека в чат /api/chats/<int:pk>/invite/ (POST)
  - Принять приглашение /api/chats/<int:pk>/accept_invite/ (POST)
  - Отклонить приглашение /api/chats/<int:pk>/reject_invite/ (POST)
  - Покинуть чат /api/chats/<int:pk>/leave/ (POST)
  
  - ? Вступление человек в чат, если он открытый то просто вступит, если закрытый то должен подтвердить модератор/админ. А если платный, то надо еще оплатить дополнительно
  - ? Создание ссылки на чат (для дальнейшего вступления или приглашения). Если чат бесплатный то просто по этой ссылке можно зайти (сразу делает accepted). Если  платный, то все равно сначала нужно оплатить. В откртых чатах эту ссылку могут создавать все, в закртых только админы/модераторы
  - ? Блокировака пользователей в группы/канале. Логика с блокировкой каналов/direct сообщений где-то в другом месте будет (пока хз)

- MESSAGE'S API:
  - Создание сообщения в чате: /api/chats/<int:chat_id>/messages/ (POST)
  - Получения списка сообщений из чата: /api/chats/<int:chat_id>/messages/ (GET)
  - Получение информации о сообщении в чате chat_id: /api/chats/<int:chat_id>/messages/<int:pk> (GET)
  - Обновлении информации о сообщении: /api/chats/<int:chat_id>/messages/<int:pk> (PATCH/PUT)
  - Удаление сообщения: /api/chats/<int:chat_id>/messages/<int:pk> (DELETE)

  - ? Получение списка всех сообщений с каким-то фильтром: /api/messages/ (GET)



## Chat

# list: GET /api/chats/
- Возвращает список чатов, в которых пользователь состоит с invitation_status равным accepted или pending. Чаты сортируются по last_message_time (убывание) и id
  Input: {}
  Output:
    В ответ получает массив [] объектов типа ChatListSerializer:
    [
      {
        id: number;
        chat_type: "direct" | "group" | "channel";
        title: string;
        last_message: null | {
          id: number;
          content: string;
          created_at: string;
          sender_username: string;
          is_read: boolean;
        }; 
        channel_settings: null | {
          is_public: boolean;
          is_paid: booleand;
          monthly_price: string;
        };
      },
    ]
    
# create: POST /api/chats/
- Создание нового чата. Набор входных данных зависит от типа чата
  Input:
    chat_type == "direct":
    {
      chat_type: "direct";
      title: string;
      description?: string;
      new_participants: [ number ]; // ровно один id другого пользователя (не должен совпадать с id создателя)
    }
    chat_type == "group":
    {
      chat_type: "group";
      title: string;
      description?: string;
      new_participants?: number[]; // список id пользователей
    }
    chat_type == "channel":
    {
      chat_type: "channel";
      title: string;
      description?: string;
      new_participants?: number[]; // список id пользователей
      channel_settings?: {
        is_public?: boolean;
        is_paid?: boolean;
        monthly_price?: string;
      } | null;
    }
  Output:
    В ответ получает объект типа ChatCreateSerializer:
    {
      id: number;
      chat_type: "direct" | "group" | "channel";
      title: string;
      description: string | null;
      created_at: string;
      participants: [
        {
          id: number;
          chat: number;
          user: number;
          role: "admin" | "moderator" | "member" | "subscriber";
          joined_at: string;
          invitation_status: "pending" | "accepted" | "rejected";
          is_blocked: boolean;
        },
        ...
      ];
      channel_settings: null | {
        is_public: boolean;
        is_paid: booleand;
        monthly_price: string;
      };
    }


- Обращаться может только пользователь состоящий в участиниках и имеюший статус "pending" | "accepted"

# retrieve GET /api/chats/<int:pk>/
- Получение детальной информации о чате по id. Если у пользователя статус pending, возвращается сокращённое представление (только id, chat_type и title):
  Input: {}
  Output: 
    В ответ получает объект типа ChatSerializer:
    {
      id: number;
      chat_type: "direct" | "group" | "channel";
      title: string;
      description: string | null;
      created_at: string;
      participants: [
        {
          id: number;
          chat: number;
          user: number;
          role: "admin" | "moderator" | "member" | "subscriber";
          joined_at: string;
          invitation_status: "pending" | "accepted" | "rejected";
          is_blocked: boolean;
        },
        ...
      ];
      channel_settings: null | {
        is_public: boolean;
        is_paid: booleand;
        monthly_price: string;
      };
    }

# update PATCH/PUT /api/chats/<int:pk>/
- Обновление данных чата (только для group и channel; direct-чаты обновлять нельзя). Только участники со статусом accepted и ролью admin или moderator
  Input:
    {
      title? :string;
      description?: string;
      channel_settings?: {
        is_public?: boolean;
        is_paid?: booleand;
        monthly_price?: string;
      };
    }
  Output: 
    В ответ получает объект типа ChatSerializer:
    {
      id: number;
      chat_type: "direct" | "group" | "channel";
      title: string;
      description: string | null;
      created_at: string;
      participants: [
        {
          id: number;
          chat: number;
          user: number;
          role: "admin" | "moderator" | "member" | "subscriber";
          joined_at: string;
          invitation_status: "pending" | "accepted" | "rejected";
          is_blocked: boolean;
        },
        ...
      ];
      channel_settings: null | {
        is_public: boolean;
        is_paid: booleand;
        monthly_price: string;
      };
    }

# destroy DELETE /api/chats/<int:pk>/
- Удаление чата по id, могут делать только участники с role == "admin" и status == "accepted"  и если chat_type != "direct"
  Input: {}
  Output: {} | success 204


# invite POST /api/chats/<int:pk>/invite
- Приглашение пользователя в чат (для group и channel; direct-чаты не поддерживают приглашения). Для channel, если channel_settings.is_public = false, приглашать могут только участники с ролью admin или moderator
  Input:
    {
      user_id: number;
    }
  Output:
    {
      detail: "User invited with status 'pending'."
    }

# invite POST /api/chats/<int:pk>/invite
- Приглашение пользователя в чат (для group и channel; direct-чаты не поддерживают приглашения). Для channel, если channel_settings.is_public = false, приглашать могут только участники с ролью admin или moderator. Если пользователь уже является участником или приглашение уже отправлено, возвращается ошибка.
  Input:
    {
      user_id: number;
    }
  Output:
    {
      detail: "User invited with status 'pending'."
    }

# accept_invite POST /api/chats/<int:pk>/accept_invite
- Принятие приглашения в чат (смена статуса с pending на accepted). Пользователь должен иметь статус pending
  Input: {}
  Output:
    {
      detail: "Invitation accepted."
    }

# reject_invite POST /api/chats/<int:pk>/reject_invite
- Отклонение приглашения в чат (смена статуса с pending на rejected).Пользователь должен иметь статус pending
  Input: {}
  Output:
    {
      detail: "Invitation accepted."
    }

# leave POST /api/chats/<int:pk>/leave
- Покинуть чат (применимо для group и channel; direct-чаты нельзя покинуть)
  Input: {}
  Output:
    {
      detail: "You have left the chat."
    }


## Message

# list: GET /api/chats/<int:chat_id>/messages/
- Получение списка сообщений в чате. 
  Input: {}
  Output:
    В ответ получает массив [] объектов типа MessageSerializer:
    [
      {
        id: number;
        chat: number;
        sender: number;
        sender_username: string;
        content: string;
        created_at: string;
        is_read: boolean;
        is_edited: boolean;
      },
      ...
    ]

# create: POST /api/chats/<int:chat_id>/messages/
- Создание нового сообщения в чате chat_id (POST). После создания сообщения обновляются поля last_message и last_message_time чата
  Input:
    {
      content: string;
    }
  Ouput:
    В ответ получаем объект типа MessageSerializer:
    {
      id: number;
      chat: number;
      sender: number;
      sender_username: string;
      content: string;
      created_at: string;
      is_read: boolean;
      is_edited: boolean;
    }


- Сюда могут обращаться только пользователи состоящие в чате с ID chat_id и со статусом "accepted". Не заблоченные is_blocked=False.

# retrieve: GET /api/chats/<int:chat_id>/messages/<int:pk>/
- Детальная информация о сообщении с ID pk в чате chat_id (GET)
  Input: {}
  Output:
    В ответ получаем объект типа MessageSerializer:
    {
      id: number;
      chat: number;
      sender: number;
      sender_username: string;
      content: string;
      created_at: string;
      is_read: boolean;
      is_edited: boolean;
    }

# update: PATH/PUT /api/chats/<int:chat_id>/messages/<int:pk>/
- Обновление содержания сообщения. Только отправитель сообщения (IsMessageSender). При изменении текста устанавливается флаг is_edited в true
  Input:
    {
      content: "string";
    }
  Output:
    В ответ получаем объект типа MessageSerializer:
    {
      id: number;
      chat: number;
      sender: number;
      sender_username: string;
      content: string;
      created_at: string;
      is_read: boolean;
      is_edited: true;
    }

# destroy: DELETE /api/chats/<int:chat_id>/messages/<int:pk>/
- Удаление сообщения. Для direct-чата: удалять может только отправитель. Для group/channel: удалять может отправитель или участники с ролью admin/moderator. Если удаляемое сообщение является последним в чате, обновляются поля last_message и last_message_time
  Input: {}
  Output: {} | success 204
  

  