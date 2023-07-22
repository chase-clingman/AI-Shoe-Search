<template>
  <!-- Q-form for the search input -->
  <q-form style="width: 100%; max-width: 1200px" class="form center">
    <q-input
      outlined
      v-model="localSearchText"
      label="e.g. apartment with living room that gets a lot of light"
      style="width: 100%; max-width: 1600px"
    >
      <template v-slot:append>
        <q-btn
          flat
          class="search-button-input"
          icon="search"
          type="submit"
          @click="searchImage"
        />
      </template>
    </q-input>
  </q-form>

  <div class="q-mt-xl exampleDiv">
    <!-- <div class="expansion text-center">Search Examples</div>
    <div flat class="row q-gutter-md cards-container q-my-sm">
      <q-card
        flat
        class="expansionCard"
        @click="
          sendText(
            `Find a pair of Air Jordans with a patent leather upper and Chicago Bulls red colorway`
          )
        "
      >
        <q-icon
          name="settings_suggest"
          class="cardIcon text-center center"
          size="45px"
        />
        <div class="cardTitle">Feature Based</div>
        <div class="cardExample">
          "Find a pair of Air Jordans with a patent leather upper and Chicago Bulls red colorway."
        </div>
        <q-icon name="east" class="cardArrow text-center center" size="20px" />
      </q-card>
      <q-card
        flat
        class="expansionCard"
        @click="
          sendText(
            `Find a pair of Yeezy Boost 350s with a ribbed sole, reflective details, and a sock-like construction`
          )
        "
      >
        <q-icon
          name="handyman"
          class="cardIcon text-center center"
          size="45px"
        />
        <div class="cardTitle">Structural</div>
        <div class="cardExample">
          "Find a pair of Yeezy Boost 350s with a ribbed sole, reflective details, and a sock-like construction."
        </div>
        <q-icon name="east" class="cardArrow text-center center" size="20px" />
      </q-card>
      <q-card
        flat
        class="expansionCard"
        @click="
          sendText(
            `Find a pair of sneakers that Lil Uzi Vert would wear`
          )
        "
      >
        <q-icon
          name="interests"
          class="cardIcon text-center center"
          size="45px"
        />
        <div class="cardTitle">Abstract</div>
        <div class="cardExample">
          "Find a pair of sneakers that Lil Uzi Vert would wear."
        </div>
        <q-icon name="east" class="cardArrow text-center center" size="20px" />
      </q-card>
    </div> -->
  </div>

  <!-- Loading spinner shown while waiting for search results -->
  <q-spinner-clock
    size="4em"
    color="black"
    class="loading center text-center"
  />
  <!-- Container for displaying the image search results -->
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
</template>

<script>
import axios from "axios";
import { Configuration, OpenAIApi } from "openai";

export default {
  props: {
    searchText: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      localSearchText: this.searchText,
      imageUrls: [],
      doc: null,
      images: [],
      currentSlide: [],

      loading: [],

      OPENAI_API_KEY: "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",

      showContent: true,
    };
  },
  watch: {
    searchText(newVal) {
      this.localSearchText = newVal;
    },
  },
  methods: {
    // Method for searching images based on the input text
    async searchImage() {
      if (!this.localSearchText) return;

      document.querySelector(".exampleDiv").style.display = "none";
      // Show loading spinner and hide the image container
      document.querySelector(".loading").style.display = "block";
      document.querySelector(".results-container").style.display = "none";

      try {
        // Make a POST request to the server with the search text
        const response = await axios.post(
          "http://127.0.0.1:5000/search",
          {
            query: this.localSearchText,
          }
        );

        // Process the response data and extract the image URLs and document data
        this.imageUrls = response.data.map((result) => {
          const images = result.doc_data.images || []; // Use the Images array from the document data
          return {
            images,
            doc: result.doc_data,
          };
        });

        this.loading = [];
        for (let i = 0; i < this.imageUrls.length; i++) {
          this.loading.push(true);
        }

        // Initialize the currentSlide array with the correct number of elements
        this.currentSlide = [];
        for (let i = 0; i < this.imageUrls.length; i++) {
          this.currentSlide.push(0);
        }

        console.log("Received similar image URLs:", this.imageUrls);

        // Show the image container and hide the loading spinner
        document.querySelector(".results-container").style.display = "block";
        document.querySelector(".loading").style.display = "none";

        // Generate summaries for the apartment descriptions
        // await this.sumGenerator();

        console.log(this.imageUrls);
      } catch (error) {
        // Log the error and hide the loading spinner
        console.error("Error searching image:", error);
        document.querySelector(".loading").style.display = "none";
      }
    },

    // Method for generating summaries of the apartment descriptions
    // async sumGenerator() {
    //   // Loop through each item in imageUrls
    //   for (let i = 0; i < this.imageUrls.length; i++) {
    //     let input = this.imageUrls[i].doc["Content Text"];
    //     // Make a completion call to the OpenAI API to generate a summary
    //     await this.completionCall(
    //       "summarize this information in around 60 words. \nThe start of the summary should revolve around this: " +
    //         this.searchText +
    //         "\nSummarize this:\n " +
    //         input
    //     );
    //     // Update the apartment description with the generated summary
    //     this.imageUrls[i].doc["Content Text"] = this.response;
    //     this.loading[i] = false;
    //   }
    // },
    // Method for making a completion call to the OpenAI API
    async completionCall(input) {
      let messages = [];
      messages.push({ role: "user", content: input });

      const apiKey = process.env.OPENAI_API_KEY || this.OPENAI_API_KEY;
      const apiEndpoint = "https://api.openai.com/v1/chat/completions";

      const headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      };

      const data = {
        model: "gpt-3.5-turbo",
        messages: messages,
      };

      let attempts = 3;
      let success = false;

      // Retry the API call up to 3 times in case of failure
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

    // Method to download apartment data as a CSV
    downloadCSV(data, fileName) {
      // Convert the JSON object to a CSV string
      const csvData = this.jsonToCSV(data);

      // Create a Blob object with the CSV data and set the MIME type to text/csv
      const blob = new Blob([csvData], { type: "text/csv" });

      // Create a temporary anchor element to initiate the download
      const downloadLink = document.createElement("a");
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = `${fileName}.csv`;

      // Add the link to the DOM, click it, and remove it
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    },

    // Method to convert JSON to CSV
    // Method to convert JSON to CSV
    jsonToCSV(jsonData) {
      const keys = Object.keys(jsonData);
      const values = Object.values(jsonData);
      let csvArray = [];

      // Add the header row
      csvArray.push(keys.join(","));

      // Add the data row
      const dataRow = values.map((value) => {
        if (value[0] && typeof value[0] === "string") {
          return value[0].replace(/,/g, ";"); // Replace commas with semicolons to avoid breaking the CSV format
        } else {
          return value[0];
        }
      });
      csvArray.push(dataRow.join(","));

      // Convert the array to a CSV string
      return csvArray.join("\n");
    },

    sendText(input) {
      this.localSearchText = input;
      this.searchImage();

      // this.showContent = false;
    },
  },
};
</script>

<style>
.center {
  display: block;
  margin-top: 25px;
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

.search-input {
  width: 80%;
  margin-bottom: 1rem;
}

.search-button {
  margin-bottom: 2rem;
}

.result-card {
  width: 460px;
  height: 300px;
  overflow: hidden;
  padding: 0;
  border-bottom: 1px solid #ddd;
  transition: all 0.1s ease-in-out;
}
.result-card:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  transform: scale(1.02);
  cursor: pointer;
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

.search-button-input {
  background-color: #f04845;
  color: white;
  height: 100%;
  border-radius: 0;
  position: relative;
  left: 12px;
}
</style>
