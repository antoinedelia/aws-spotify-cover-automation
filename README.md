<h1 align=center>Spotify Cover Automation | <a href="https://spotify-cover.antoinedelia.fr/" rel="nofollow">Website</a></h1>

<p align="center"><b>Elevate your Spotify playlists with unique, automatically generated cover art!</b> ✨</p>

<p align="center">
  <img width="450" alt="image" src="https://github.com/user-attachments/assets/7619df37-6eb5-4313-bbb3-8d9020c06693" />
</p>


This tool analyzes your chosen Spotify playlist, identifies the **top 4 most frequent artists**, and then crafts a beautiful custom cover image for your playlist. Best of all, it can **automatically update the playlist cover on Spotify** for you. Give your playlists the visual identity they deserve!

## 🌟 Features

* **Top Artist Detection:** Automatically identifies the 4 most prominent artists in your selected Spotify playlist.
* **Custom Cover Generation:** Creates a unique cover image design incorporating elements related to the top artists (e.g., artist images, names, or a stylized collage).
* **Automatic Spotify Update:** Seamlessly updates your chosen playlist's cover image directly on Spotify.
* **Simple Web Interface:** Easy-to-use interface built with HTML, CSS, and JavaScript for a smooth user experience.
* **Serverless Backend:** Powered by AWS for scalability and reliability.
* **Infrastructure as Code:** Deployed and managed using the AWS Cloud Development Kit (CDK).
* **Open Source:** Contribute to the project and help make it even better!

## 🛠️ Tech Stack

This project leverages a modern, cloud-native architecture:

* **Frontend:**
    * HTML
    * CSS
    * JavaScript
* **Backend & Infrastructure:**
    * AWS Lambda (for serverless functions handling artist analysis, image generation, and Spotify API interaction)
    * Amazon API Gateway (for API exposure)
    * Amazon S3 (for hosting the static frontend and potentially temporary image storage)
    * Amazon CloudFront (for content delivery and HTTPS)
    * AWS IAM (for secure access management)
    * AWS Cloud Development Kit (CDK) (for defining and deploying cloud infrastructure in TypeScript/Python)
* **Spotify API:** Used for accessing playlist data, artist information, and updating playlist cover images.

## 🚀 Getting Started (For Users)

1.  **Visit the website:** [https://spotify-cover.antoinedelia.fr/](https://spotify-cover.antoinedelia.fr/)
2.  **Authenticate with Spotify:** You'll be prompted to log in to your Spotify account to grant necessary permissions (to read your playlists and update their cover images).
3.  **Select Your Playlist:** Choose the playlist for which you want to generate a new cover.
4.  **Update Playlist Cover:** The tool will analyze the playlist, detect top artists, generate a the cover image and automatically update it on Spotify!
5.  **Enjoy Your Refreshed Playlist:** Check out your playlist on Spotify with its new custom art!

## 🧑‍💻 Getting Started (For Developers & Contributors)

Interested in contributing or running your own instance? Here's a general guide:

**Prerequisites:**

* [Node.js](https://nodejs.org/) (v18.x or later recommended)
* [AWS CLI](https://aws.amazon.com/cli/) configured with your credentials
* [AWS CDK](https://aws.amazon.com/cdk/) ( `npm install -g aws-cdk` )
* A Spotify Developer Account and App (to get your Client ID and Client Secret, and to set the Redirect URI) - [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
