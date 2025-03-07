import { create } from 'zustand';

interface ChatState {
  chats: number[];
  chatsById: Record<number, any>;
  messagesByChatId: Record<number, any[]>;
  clearChatState: () => void;
  addChats: (newChats: any[]) => void;
  deleteChat: (chatId: number) => void;
  addMessages: (chatId: number, newMessages: any[]) => void;
  setChatMemberCount: (chatId: number, memberCount: number) => void;
}

const initialChatState = {
  chats: [] as number[],
  chatsById: {} as Record<number, any>,
  messagesByChatId: {} as Record<number, any[]>,
};

export const useChatState = create<ChatState>((set, get) => ({
  ...initialChatState,

  clearChatState: () => set(() => ({ ...initialChatState })),

  addChats: (newChats) => set((state) => {
    const updatedChatsById = { ...state.chatsById };
    newChats.forEach((chat) => {
      if (!updatedChatsById[chat.id]) {
        updatedChatsById[chat.id] = chat;
      }
    });
    const mergedChatIds = Array.from(
      new Set([...newChats.map((chat) => chat.id), ...state.chats])
    );
    const sortedChatIds = mergedChatIds.sort((a, b) => {
      const chatA = updatedChatsById[a];
      const chatB = updatedChatsById[b];
      return chatB.last_message_time.localeCompare(chatA.last_message_time);
    });
    return {
      chats: sortedChatIds,
      chatsById: updatedChatsById,
    };
  }),

  deleteChat: (chatId) => set((state) => {
    const newChatsById = { ...state.chatsById, [chatId]: null };
    const newChats = state.chats.filter((id) => id !== chatId);
    const { [chatId]: deletedMessages, ...newMessagesByChatId } = state.messagesByChatId;
    return {
      chats: newChats,
      chatsById: newChatsById,
      messagesByChatId: newMessagesByChatId,
    };
  }),

  addMessages: (chatId, newMessages) => set((state) => {
    const currentMessages = state.messagesByChatId[chatId] || [];
    const combinedMessages = [...currentMessages, ...newMessages].filter(
      (message, index, self) =>
        index === self.findIndex((m) => m.id === message.id)
    );
    combinedMessages.sort((a, b) => a.id - b.id);
    const maxMessageId = combinedMessages.length > 0
      ? combinedMessages[combinedMessages.length - 1].id
      : null;
    let needSort = false;
    const updatedChatsById = { ...state.chatsById };
    if (
      maxMessageId !== null &&
      updatedChatsById[chatId] &&
      (!updatedChatsById[chatId].last_message ||
        maxMessageId > updatedChatsById[chatId].last_message.id)
    ) {
      const newLastMessage = combinedMessages.find(
        (message) => message.id === maxMessageId
      );
      if (newLastMessage) {
        updatedChatsById[chatId] = {
          ...updatedChatsById[chatId],
          last_message: newLastMessage,
          bumped_at: newLastMessage.chat.bumped_at,
        };
        needSort = true;
      }
    }
    let updatedChats = [...state.chats];
    if (needSort) {
      updatedChats = updatedChats.sort((a, b) => {
        const chatA = updatedChatsById[a];
        const chatB = updatedChatsById[b];
        return chatB.bumped_at.localeCompare(chatA.bumped_at);
      });
    }
    return {
      messagesByChatId: {
        ...state.messagesByChatId,
        [chatId]: combinedMessages,
      },
      chatsById: updatedChatsById,
      chats: updatedChats,
    };
  }),

  setChatMemberCount: (chatId, memberCount) => set((state) => {
    if (!state.chatsById[chatId]) {
      console.error(`Chat with ID ${chatId} not found.`);
      return state;
    }
    const updatedChat = {
      ...state.chatsById[chatId],
      member_count: memberCount,
    };
    return {
      chatsById: {
        ...state.chatsById,
        [chatId]: updatedChat,
      },
    };
  }),
}));