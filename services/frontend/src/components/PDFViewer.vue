<template>
  <div>
    <pdf
      :src="pdfdata"
      v-for="i in numPages"
      :key="i"
      :id="i"
      :page="i"
      :scale.sync="scale"
      style="width: 100%; margin: 20px auto"
      :annotation="true"
      :resize="true"
    >
      <template slot="loading"> loading content here... </template>
    </pdf>
  </div>
</template>

<script>
import pdfvuer from "pdfvuer";
import "pdfjs-dist/build/pdf.worker.entry"; // not needed since v1.9.1

export default {
  components: {
    pdf: pdfvuer,
  },
  data() {
    return {
      page: 1,
      numPages: 0,
      pdfdata: undefined,
      errors: [],
      scale: "page-width",
    };
  },
  props: {
    pdfpath: {
      type: String,
      default:
        "https://file-examples-com.github.io/uploads/2017/10/file-example_PDF_1MB.pdf",
    },
  },
  watch: {
    pdfpath: function () {
      this.resetData();
      this.getPdf();
    },
  },
  methods: {
    resetData() {
      this.page = 1;
      this.numPages = 0;
      this.pdfdata = undefined;
      this.errors = [];
    },
    getPdf() {
      var self = this;
      self.pdfdata = pdfvuer.createLoadingTask(
        "http://localhost:5001/file/" + this.pdfpath
      );
      self.pdfdata.then((pdf) => {
        self.numPages = pdf.numPages;
      });
    },
  },
};
</script>
