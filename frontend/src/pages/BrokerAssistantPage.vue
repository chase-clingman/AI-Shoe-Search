<template>
  <q-page class="flex flex-center column">
    <div class="hero q-ma-lg text-center">
      YOUR PERSONALIZED <br />BROKER ASSISTANT
    </div>
    <div class="input-container" @click="triggerInput">
      <div class="file-type">
        <img
          v-if="image"
          :src="previewUrl"
          alt="Selected image"
          class="preview-image"
        />
        <q-icon v-else name="image" size="2em" />
      </div>
      <input
        type="file"
        accept="image"
        ref="imageInput"
        @change="selectImage"
        hidden
      />
    </div>
    <q-btn
      class="upload-button"
      unelevated
      color="primary"
      @click="describeImage"
    >
      Upload Image
    </q-btn>
    <div class="loading">
      <q-spinner-clock size="4em" color="primary" class="center text-center" />
      <div class="text-h5 q-ma-sm text-center">Generating Copyright...</div>
    </div>
    <q-card style="max-width: 1200px;" class="copyCard">
      <div class="copyright">
        <div class="q-ma-sm">
          {{ descriptions }}
        </div>
      </div>
    </q-card>
  </q-page>
</template>

<script>
import axios from "axios";
import { Configuration, OpenAIApi } from "openai";

export default {
  // name: 'PageName',
  data() {
    return {
      image: null,
      descriptions: "",
      OPENAI_API_KEY: "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",
    };
  },
  computed: {
    previewUrl() {
      return this.image ? URL.createObjectURL(this.image) : null;
    },
  },
  methods: {
    triggerInput() {
      this.$refs.imageInput.click();
    },
    async selectImage() {
      this.image = this.$refs.imageInput.files[0];
    },
    async describeImage() {
      if (!this.image) return;

      document.querySelector(".loading").style.display = "block";

      const formData = new FormData();
      formData.append("image", this.image);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/describe_image",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );

        const descriptions = response.data.descriptions;
        console.log("Received image descriptions:", descriptions);

        this.descriptions = descriptions;
        await this.completionCall("You are a broker assistant. Please provide copyright describing an image that has these descriptions: " + this.descriptions).then(() => {
          this.descriptions = this.response;
          document.querySelector(".copyCard").style.display = "block";
        });

        document.querySelector(".loading").style.display = "none";
      } catch (error) {
        console.error("Error uploading image:", error);
        document.querySelector(".loading").style.display = "none";
      }
    },
    async completionCall(input) {
      let messages = [];
      messages.push({ role: "user", content: input });

      const apiKey = process.env.OPENAI_API_KEY || this.OPENAI_API_KEY;
      const apiEndpoint = "https://api.openai.com/v1/chat/completions"; // Update the endpoint according to the API version you're using

      const headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      };

      const data = {
        model: "gpt-4", // USE THIS MODEL FOR NOW FOR FASTER RESPONSES
        messages: messages,
      };

      let attempts = 3;
      let success = false;

      while (attempts > 0 && !success) {
        try {
          const response = await axios.post(apiEndpoint, data, { headers });
          const completion = response.data;
          this.response = completion.choices[0].message.content;
          messages.push({
            role: completion.choices[0].message.role,
            content: this.response,
          });
          console.log(this.response);
          success = true;
        } catch (error) {
          console.error("API call failed:", error);
          attempts--;
          if (attempts > 0) {
            console.log("Retrying... attempts left:", attempts);
          }
        }
      }

      if (!success) {
        console.error("Failed after 3 attempts");
        // Handle the case when all attempts fail
      }
    },
  },
};
</script>
<style>
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
}
.hero {
  font-family: "Roboto", sans-serif;
  font-size: 3rem;
  font-weight: 500;
  letter-spacing: 0.2rem;
  color: #535151;
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
  width: 400px;
  height: 400px;
  background-color: #eee;
  border: 2px dashed #999;
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
}
.loading {
  display: none;
}

.copyright {
  white-space: pre-wrap;
  font-family: "Roboto", sans-serif;
  font-size: 20px;
  font-weight: 300;
  color: #535151;
}
.copyCard {
  display: none;
}
</style>
