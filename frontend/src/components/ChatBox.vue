<template>
  <div class="flex flex-col bg-white rounded-xl shadow p-4 h-96">
    <div class="flex-grow overflow-y-auto space-y-2 pr-1">
      <div
        v-for="(m, i) in messages"
        :key="i"
        class="flex"
        :class="m.from === 'me' ? 'justify-end' : 'justify-start'"
      >
        <div
          class="px-3 py-2 rounded-lg max-w-xs text-sm"
          :class="m.from === 'me'
            ? 'bg-blue-500 text-white'
            : 'bg-gray-200 text-gray-800'"
        >
          {{ m.text }}
        </div>
      </div>
    </div>

    <div class="flex mt-3">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Написать сообщение..."
        class="flex-grow border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-300"
        @keyup.enter="sendMessage"
      />
      <button
        class="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600"
        @click="sendMessage"
      >
        Отправить
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatBox",
  props: {
    userRole: {
      type: String,
      default: "participant"
    }
  },
  data() {
    return {
      messages: [],
      newMessage: ""
    };
  },
  methods: {
    sendMessage() {
      if (!this.newMessage.trim()) return;

      this.messages.push({
        text: this.newMessage,
        from: this.userRole === "owner" ? "me" : "me"
      });

      this.newMessage = "";

      this.$nextTick(() => {
        const el = this.$el.querySelector(".overflow-y-auto");
        el.scrollTop = el.scrollHeight;
      });
    }
  }
};
</script>
