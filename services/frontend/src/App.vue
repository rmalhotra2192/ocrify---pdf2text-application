<template>
  <div id="app">
    <OCRRecognizedText :content="recognizedText"></OCRRecognizedText>
  </div>
</template>

<script>
import OCRRecognizedText from "@/components/OCRRecognizedText.vue";

export default {
  data() {
    return {
      recognizedText: "Test Data",
    };
  },
  components: {
    OCRRecognizedText,
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.ocrtext-container {
  height: 550px;
  overflow-y: scroll;
}
</style>
