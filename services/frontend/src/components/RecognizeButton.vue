<template>
  <div class="flex w-full items-center justify-center bg-gray">
    <label
      class="w-64 flex flex-col items-center px-4 py-6 bg-white text-blue-500 rounded-lg shadow-lg tracking-wide uppercase border border-blue-500 cursor-pointer hover:bg-blue-500 hover:text-white"
      @click="sendRequestToRunOCR"
    >
      <img src="@/assets/phone.png" class="w-8 h-8" />
      <span class="mt-2 text-base leading-normal">Recognize</span>
    </label>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    pdfid: {
      type: String,
      required: true,
      default: "",
    },
  },
  methods: {
    sendRequestToRunOCR() {
      var baseURL = "http://127.0.0.1:8000";

      axios
        .get(baseURL + "/runocronpdf/" + this.pdfid)
        .then((data) => {
          console.log(data);
          this.$emit("task-submitted", data["data"]["task_id"]);
        })
        .catch(() => {
          console.log("FAILURE!!");
        });
    },
  },
};
</script>

<style lang="scss" scoped></style>
