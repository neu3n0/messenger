# Желаемый функционал

- CHAT'S API:
  - Создание чата: /api/chats/ (POST)
  - Получение списка чатов: /api/chats/ (GET)
  - Получение информации о чате: /api/chats/<int:pk>/ (GET)
  - Обновлении инофрмации о чате: /api/chats/<int:pk>/ (PATCH/PUT)
  - Удаление чата: /api/chats/<int:pk>/ (DELETE)
  
  
  - ? Приглашение человека в чат
  - ? Вступление человек в чат, если он открытый
  - ? Создание ссылки на чат (для дальнейшего вступления или приглашения)
  - ? Покинуть чат
  - ? Заблокировать чат

- MESSAGE'S API:
  - Создание сообщения в чате: /api/chats/<int:chat_id>/messages/ (POST)
  - Получения списка сообщений из чата: /api/chats/<int:chat_id>/messages/ (GET)
  - Получение информации о сообщении в чате chat_id: /api/chats/<int:chat_id>/messages/<int:pk> (GET)
  - Обновлении информации о сообщении: /api/chats/<int:chat_id>/messages/<int:pk> (PATCH/PUT)
  - Удаление сообщения: /api/chats/<int:chat_id>/messages/<int:pk> (DELETE)


  - ? Получение списка всех сообщений с каким-то фильтром: /api/messages/ (GET)







# ChatListCreateView: /api/chats/

- Список чатов (GET), где у пользователя invitation_status = accepted или pending.
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
    

- Создание чата (POST):
  Input:
    Если chat_type == "direct" надо передать в body обязательно передать в new_participants ровно одного участника:
    {
      chat_type: "direct";
      title: string;
      new_participants: [
        int
      ];
      description?: string;
    }
    Если chat_type == "group":
    {
      chat_type: "channel";
      title: string;
      new_participants?: [
        int,
        int,
        ...
      ];
      description?: string;
    }
    Если chat_type == "channel" можно передать доп. поля в body для настройки канал:
    {
      chat_type: "channel";
      title: string;
      new_participants?: [
        int,
        int,
        ...
      ];
      description?: string;
      channel_settings?: null | {
        is_public?: boolean;
        is_paid?: booleand;
        monthly_price?: string;
      };
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

# ChatRetrieveUpdateDestroyView: /api/chats/<int:pk>/
- Обращаться может только пользователь состоящий в участиниках и имеюший статус "pending" | "accepted"

- Детальная информация о конкретном чате по pk (GET):
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

- Обновление данных чата (PATCH/PUT), могут отправлять только люди с role == "admin" | "moderator" и status == "accepted" и если chat_type != "direct"
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

- Удаление чата по id (DELETE), могут делать только участники с role == "admin" и status == "accepted"  и если chat_type != "direct"
  Input: {}
  Output: {} | error? | success?





# MessageListCreateView /api/chats/<int:chat_id>/messages/

- Список всех сообщений конкретного чата chat_it (GET). 
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

- Создание нового сообщения в чате chat_id (POST)
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

# MessageRetrieveUpdateDestroyView /api/chats/<int:chat_id>/messages/<pk>/
- Сюда могут обращаться только пользователи состоящие в чате с ID chat_id и со статусом "accepted". Не заблоченные is_blocked=False.


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

- Обновление сообщения (PATH/PUT). Может делать только sender. (!!! Тут имеет смысл наверное возвращать только часть полей: типо conent и is_edited)  
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
- Удаление сообщения (DELETE). Разрешено, если текущий пользователь – отправитель или имеет роль "admin"/"moderator". Если удаляетя последнее собщение, то оно пересчитывается в Chat.
  Input: {}
  Output: {} | error | success
  

  