<template>
  <div
    :class="{ 'h-screen': active }"
    class="upload-pdf-button flex w-full items-center justify-center bg-gray"
  >
    <label
      class="w-64 flex flex-col items-center px-4 py-6 bg-white text-blue-500 rounded-lg shadow-lg tracking-wide uppercase border border-blue-500 cursor-pointer hover:bg-blue-500 hover:text-white"
    >
      <svg
        class="w-8 h-8"
        fill="currentColor"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
      >
        <path
          d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z"
        />
      </svg>
      <span class="mt-2 text-base leading-normal">{{ buttonText }}</span>
      <input
        type="file"
        id="file"
        ref="file"
        class="hidden"
        v-on:change="handleFileUpload()"
      />
    </label>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      file: "",
    };
  },
  props: {
    buttonText: {
      type: String,
      default: "Upload File",
    },
    active: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    submitFile() {
      let formData = new FormData();
      formData.append("file", this.file);

      var baseURL = "http://127.0.0.1:5001";

      let config = {
        header: {
          "Content-Type": "multipart/form-data",
        },
      };

      axios
        .post(baseURL + "/uploadfile", formData, config)
        .then((data) => {
          console.log(data);
          console.log("SUCCESS!!");
          this.$emit("uploaded", data["data"]);
        })
        .catch(() => {
          console.log("FAILURE!!");
        });

      console.log(formData);
    },

    handleFileUpload() {
      this.file = this.$refs.file.files[0];
      this.submitFile();
    },
  },
};
</script>

<style lang="scss" scoped></style>
