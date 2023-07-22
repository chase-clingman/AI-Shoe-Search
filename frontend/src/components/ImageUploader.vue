<template>
  <div class="container">
    <div class="upload-container">
      <div class="input-container">
        <div class="upload-header">
          Upload your images to find similar apartments
        </div>
        <div class="icon-container" @click="triggerInput">
          <q-icon
            v-if="!previewUrl"
            name="o_cloud_upload"
            size="7em"
            style="color: #333333b2"
          />
          <img
            v-else
            :src="previewUrl"
            alt="Selected Image"
            class="selected-image"
          />
          <div class="file-text" v-if="!previewUrl">
            Drag and drop or click to browse and choose a file
          </div>
        </div>

        <input
          type="file"
          accept="image"
          ref="imageInput"
          @change="selectImage"
          hidden
        />
        <div class="button-container">
          <q-btn
            class="upload-button"
            unelevated
            color="primary"
            @click="uploadImage"
          >
            Search
          </q-btn>
        </div>
      </div>
    </div>
    <!--
    <q-btn
      class="upload-button"
      unelevated
      color="primary"
      @click="uploadImage"
    >
      Upload Image
    </q-btn> -->
    <q-spinner-clock
      size="4em"
      color="black"
      class="loading center text-center"
    />
    <div class="results-container center">
      <!-- Wrapper for the result cards -->
      <div class="card-wrapper" style="width: 100%">
        <!-- Loop through each image result and create a card -->
        <a
          v-for="(result, index) in imageUrls"
          :key="index"
          :href="result.doc['url']"
          target="_blank"
          style="text-decoration: none; color: black; width: 100%"
        >
          <q-card
            class="q-mx-lg result-card flex items-center"
            style="width: 100%"
            flat
          >
            <div class="row q-gutter-lg" style="width: 100%">
              <div class="d-flex justify-center items-center">
                <q-card-section v-if="result.doc">
                  <q-img :src="result.doc['Image URL']" style="width: 400px" />
                </q-card-section>
              </div>
              <div class="d-flex flex-column justify-center col-3">
                <q-card-section class="text-left" v-if="result.doc">
                  <div class="text-h5 q-mt-md">
                    {{ result.doc["Price"] }}
                  </div>
                  <div class="text-body1 q-mt-sm">
                    {{ result.doc["Shoe Name"] }}
                  </div>
                  <!-- <div class="text-subtitle2">
                {{ result.doc["Bed Count"] }} | {{ result.doc["Bath Count"] }} |
                {{ result.doc["Square Feet"] }}
              </div> -->
                </q-card-section>
                <q-btn
                  v-if="result.doc"
                  color="primary"
                  icon="o_shopping_cart"
                  label="Buy Now"
                  no-caps
                  class="text-white text-body1 text-bold d-flex justify-center q-mt-md"
                  @click="
                    downloadCSV(result.doc, result.doc['Building Title'][0])
                  "
                />
              </div>
            </div>
            <!-- <q-separator  /> -->
          </q-card>
        </a>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  data() {
    return {
      image: null,
      description: null,
      imageUrls: [],
      doc: null,
      images: [],
      currentSlide: [],
    };
  },
  computed: {
    previewUrl() {
      return this.image ? URL.createObjectURL(this.image) : null;
    },
  },
  created() {
    window.addEventListener('paste', this.handlePaste);
  },
  beforeUnmount() {
    window.removeEventListener('paste', this.handlePaste);
  },
  methods: {
    handlePaste(e) {
      const items = (e.clipboardData || e.originalEvent.clipboardData).items;
      for (let index in items) {
        const item = items[index];
        if (item.kind === "file") {
          const blob = item.getAsFile();
          this.selectImageFromFile(blob);
          break;
        }
      }
    },
    selectImageFromFile(file) {
      this.image = file;
    },
    async selectImage() {
      if (this.$refs.imageInput.files.length > 0) {
        this.selectImageFromFile(this.$refs.imageInput.files[0]);
      }
    },
    triggerInput() {
      this.$refs.imageInput.click();
    },
    // async selectImage() {
    //   this.image = this.$refs.imageInput.files[0];
    // },
    async uploadImage() {
      if (!this.image) return;

      document.querySelector(".loading").style.display = "block";

      const formData = new FormData();
      formData.append("image", this.image);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/process_image",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );
        this.imageUrls = response.data.map((result) => {
          const images = result.doc_data.images || []; // Use the Images array from the document data
          return {
            images,
            doc: result.doc_data,
          };
        });

        // Initialize the currentSlide array with the correct number of elements
        this.currentSlide = [];
        for (let i = 0; i < this.imageUrls.length; i++) {
          this.currentSlide.push(0);
        }

        console.log("Received similar image URLs:", this.imageUrls);
        //await this.sumGenerator();

        document.querySelector(".loading").style.display = "none";
      } catch (error) {
        console.error("Error uploading image:", error);
        document.querySelector(".loading").style.display = "none";
      }
    },
  },
};
</script>
<style>
@import url("https://fonts.googleapis.com/css2?family=Inter&family=Lato&family=Nunito:wght@700&display=swap");
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
}
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  max-width: 100%;
  width: 100%;
}

.input-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 700px;
  height: 350px;
  background-color: #eee;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
  position: relative;
}

.file-type {
  font-size: 1.5rem;
  color: #999;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.upload-button {
  margin-bottom: 2rem;
  width: 100%;
}

.description-container {
  text-align: center;
  max-width: 80%;
  margin: 0 auto;
}

.description-title {
  font-weight: bold;
  margin-bottom: 1rem;
}

.description-text {
  font-size: 1.1rem;
  line-height: 1.5;
}

.result-card {
  width: 300px;
  height: 800px;
  overflow: hidden;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  max-width: 100%;
  width: 100%;
  margin: 0 auto;
}

.card-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.q-card-section {
  max-width: 100%;
}

.searched-image {
  max-width: 100%;
  height: auto;
}
.form {
  margin-top: 25px;
}

.loading {
  display: none;
  margin-top: 25px;
}
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  max-width: 100%;
  width: 100%;
}

.upload-header {
  font-family: "Lato";
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 24px;
  display: flex;
  align-items: center;
  text-align: center;

  color: #000000;
  margin-bottom: 10px;
}

.input-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 700px;
  height: 350px;
  background-color: #eee;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
}

.button-container {
  margin-top: 1rem;
  width: 400px;
}

.icon-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 400px;
  height: 200px;
  background-color: white;
  border: 2px dashed rgba(51, 51, 51, 0.5);
  border-radius: 4px;
  padding: 1rem;
}

.file-text {
  font-family: "Lato";
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 19px;
  display: flex;
  align-items: center;
  text-align: center;

  color: #333333;

  margin-top: 10px;
}
.result-card {
  width: 460px;
  height: 350px;
  overflow: hidden;
  padding: 0;
}
.q-card__section--vert {
  padding: 0px;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  max-width: 100%;
  width: 100%;
}

.card-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.q-card-section {
  max-width: 100%;
}

.searched-image {
  max-width: 100%;
  height: auto;
}
.form {
  margin-top: 25px;
}
.loading {
  display: none;
  margin-top: 25px;
}
.carousel-image img {
  object-fit: contain;
  object-position: center;
  max-height: 100%;
  width: auto;
}

.image-carousel {
  padding: 0;
  margin: 0;
}

.csv-btn {
  position: absolute;
  z-index: 4;
  right: 5px;
  top: 5px;
}

.results-container {
  width: 100%;
  max-width: 1400px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.cardText {
  cursor: pointer;
}
.noDecoration {
  text-decoration: none;
  color: black;
}

.selected-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}
</style>
