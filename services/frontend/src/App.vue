<template>
  <div id="app">
    <div
      v-show="!first"
      class="containers grid grid-cols-4 gap-4 w-9/12 mx-auto my-5"
    >
      <div
        class="pdfviewer-container col-span-2 border border-gray-200 shadow-md"
      >
        <PDFViewer :pdfpath="pdfID"></PDFViewer>
      </div>
      <div
        class="ocrtext-container col-span-2 border border-gray-200 shadow-md"
      >
        <OCRRecognizedText :content="recognizedText"></OCRRecognizedText>
      </div>
    </div>

    <UploadPDFButton
      v-show="first"
      class="mt-5"
      @uploaded="afterUpload"
    ></UploadPDFButton>

    <div v-show="!first" class="grid grid-cols-6 gap-4">
      <div class="col-start-2 col-span-2">
        <UploadPDFButton
          buttonText="Upload Another"
          :active="first"
          class="mt-5"
          @uploaded="afterUpload"
        ></UploadPDFButton>
      </div>
      <div class="col-start-4 col-end-6">
        <RecognizeButton
          class="mt-5"
          :pdfid="pdfID"
          @task-submitted="afterSubmission"
        ></RecognizeButton>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UploadPDFButton from "@/components/UploadPDFButton.vue";
import RecognizeButton from "@/components/RecognizeButton.vue";
import PDFViewer from "@/components/PDFViewer.vue";
import OCRRecognizedText from "@/components/OCRRecognizedText.vue";

export default {
  data() {
    return {
      pdfID: undefined,
      currentTaskID: "",
      currentTaskStatus: "",
      recognizedText: "",
    };
  },
  computed: {
    first() {
      return this.pdfID === undefined;
    },
  },
  components: {
    UploadPDFButton,
    PDFViewer,
    RecognizeButton,
    OCRRecognizedText,
  },
  methods: {
    afterUpload(pdfid) {
      this.pdfID = pdfid;
    },
    checkStatus() {
      setTimeout(() => {
        let baseURL = "http://127.0.0.1:5001";

        axios.get(baseURL + "/ocrstatus/" + this.currentTaskID).then((data) => {
          if (data["data"]["task_status"] != "PENDING") {
            this.recognizedText = data["data"]["task_result"];
            return;
          } else {
            this.checkStatus();
          }
        });
      }, 1000);
    },
    afterSubmission(taskid) {
      this.currentTaskID = taskid;
      this.checkStatus();
    },
  },
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

.pdfviewer-container,
.ocrtext-container {
  height: 550px;
  overflow-y: scroll;
}
</style>
