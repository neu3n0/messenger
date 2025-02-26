# Желаемый функционал

- Что можно делать с чатом:
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

- Что можно делать с сообщением:
  - Создание сообщения в чате: /api/chats/<int:chat_id>/messages/ (POST)
  - Получения списка сообщений из чата: /api/chats/<int:chat_id>/messages/ (GET)
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
    

- Создание чата (POST): (!!! тут наверное не нужен такой детальный ответ)
  Input:
    Если chat_type == "direct" надо передать в body user_id для второго частника:
    {
      chat_type: "direct";
      title: string;
      user_id: number;  // ID второго участника
      description?: string;
    }
    Если chat_type == "channel" можно передать доп. поля в body для настройки канал:
    {
      chat_type: "channel";
      title: string;
      description?: string;
      is_public?: boolean;
      is_paid?: boolean;
      monthly_price?: string;
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

# ChatRetrieveUpdateDestroyView: /api/chats/<int:pk>/
- Обращаться может только пользователь состоящий в участиника и имеюший статус "pending" | "accepted"

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

- Обновление данных чата (PATCH/PUT), могут отправлять только люди с role == "admin" | "moderator" и status == "accepted" (!!! тут надо еще на самом деле дать менять channel_settings, если chat_type == "channel". Мб стоит рассмотреть тут вариант приглашения через изменения participants???????)
  Input:
    {
      title? :string;
      description?: string;
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

- Удаление чата по id, могут делать только участники с role == "admin" и status == "accepted"
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
  

  