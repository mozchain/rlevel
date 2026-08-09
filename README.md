# Rlevel Carpentry Solutions

This is the repository for the **Rlevel** website (`rlevelcarpentrysolutions.com.au`).
This static website project has been set up to easily integrate designs exported from **Google Stitch**.

## Project Structure

- `index.html`: The main entry point for your website. Paste your HTML here.
- `css/style.css`: The main stylesheet. Paste your Google Stitch CSS here.
- `assets/`: A folder for you to store images, icons, and fonts.

## How to add Google Stitch Designs

1. Export your design from Google Stitch (which typically provides HTML and CSS).
2. Open `index.html` and replace the placeholder content inside the `<body>` tag with your new HTML.
3. Open `css/style.css` and replace the placeholder CSS with your new CSS.
4. If your design includes images, download them and place them in the `assets/` folder, then update the image paths in your HTML/CSS to point to `assets/your-image.png`.

## Deployment to Cloudflare Pages

Since this is a static site, deploying to Cloudflare Pages is seamless:

1. Push your code to your GitHub repository (e.g., `github.com/your-username/rlevel`).
2. Log into your [Cloudflare Dashboard](https://dash.cloudflare.com).
3. Go to **Workers & Pages** -> **Create application** -> **Pages** -> **Connect to Git**.
4. Select your `rlevel` repository.
5. Leave the **Build settings** empty (Framework preset: None, Build command: empty, Build output directory: empty/root).
6. Click **Save and Deploy**.
7. Once deployed, you can assign your custom domain `rlevelcarpentrysolutions.com.au` to this Pages project in the **Custom Domains** tab of the project settings.
