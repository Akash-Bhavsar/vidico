<template>
    <div>
      <h2>{{ heading }}</h2>
  
      <label for="imageInput" v-if="!imageUrl">
        <button @click="openImageDialog">Add Image</button>
        <input
          type="file"
          id="imageInput"
          ref="imageInput"
          style="display: none"
          @change="handleImageChange"
        />
      </label>
  
      <img v-if="imageUrl" :src="imageUrl" alt="Uploaded Preview" />  
      <img v-if="grayscaleImageUrl" :src="grayscaleImageUrl" alt="Grayscale Image" />
      <button v-if="imageUrl" @click="uploadImage">Convert to Greyscale</button>

    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        heading: "Convert Image to Greyscale",
        selectedImage: null,
        imageUrl: null,
        grayscaleImageUrl: null,
      };
    },
    methods: {
      openImageDialog() {
        this.$refs.imageInput.click();
      },
      handleImageChange(event) {
        const file = event.target.files[0];

        if (file && file.type === 'image/png') {
            this.selectedImage = file;
            this.imageUrl = URL.createObjectURL(this.selectedImage);
        } else {
            alert("Please select a PNG image.");
            this.clearSelectedImage();
        }
      },
      uploadImage() {
        const formData = new FormData();
        formData.append("image", this.selectedImage);
        axios.get("http:///127.0.0.1:8000/api/upload/",
        { crossdomain: true, formData}
        )
          .then(response => {
            this.grayscaleImageUrl = "data:image/png;base64," + response.data.grayscale_image;
          })
          .catch(error => {
            console.error("Error uploading image:", error);
            alert("Error uploading image:" + error.messsage);
            
          });
      },
      clearSelectedImage() {
      this.selectedImage = null;
      this.imageUrl = null;
    },
    },
  };
  </script>
  
  <style scoped>
  div {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    text-align: center;
  }
  
  h2 {
    color: #333;
    font-size: 1.5em;
  }
  
  label {
    cursor: pointer;
    background-color: #3498db;
    color: #fff;
    padding: 10px 15px;
    border-radius: 5px;
    font-size: 1em;
    margin-bottom: 10px;
    display: inline-block;
  }
  
  button {
    background-color: #3498db;
    color: #fff;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
  }
  
  img {
    max-width: 100%;
    margin-top: 20px;
    border-radius: 8px;
  }
  </style>
  