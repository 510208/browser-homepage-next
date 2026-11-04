<center><img src="/docs/assets/wordmarks.svg" alt="Logo" width="300" align="right" /></center>

# Browser Homepage Next

Browser Homepage Next is a pure front-end static website based on Vue, Vite, and Tailwind CSS. Its goal is to provide a customizable and unique browser homepage, interacting with the local server (https://github.com/510208/browser-homepage-next/tree/main/server) via API.

### Server (https://github.com/510208/browser-homepage-next/releases/tag/1.0.0) | Chrome Plugin | Firefox Plugin

## Features

- **Customizable Browser Homepage**: Users can freely choose background images, theme colors, font styles, and customize shortcuts and widgets.

- **Real-time Data Display:** Interacts with the local server via API to display hardware information such as CPU, memory, disk space, and network connection status.

- **Compatible with personal-website-route:** Seamlessly integrates with the [personal-website-route](https://github.com/510208/personal-website-route) project to run in a backend-less environment and protect API keys.

- **Responsive Design:** The website features a responsive design, providing a good user experience on various devices.

- **Lightweight and Fast:** Built on Vite, the website loads quickly and can be installed as a desktop application.

- **Open Source Community Support:** The project is completely open source. Contributions, questions, and suggestions are welcome. Users can participate in project development through GitHub Issues and Pull Requests.

## Project Structure Description

```text browser-homepage-next/

├── public/ # Static resources (including fonts, icons, background images, etc.)

├── dist/ # Local packaged artifacts (including assets, fonts, and weather-icons)

├── docs/ # Static hosted artifacts (pre-configured for GitHub Pages deployment)

└───src # Front-end source code

├───components # Vue components (including various widgets, shortcuts, theme switchers, etc.)

│ ├───container # Four-corner container components (including shortcuts, weather, clock, etc.)

│ ├───ui # shadcn-vue UI components (including buttons, dropdown menus, sliders, etc.)

│ └───widgets # Widget components (including weather, clock, quotes, bookmarks, etc.)

│ ├───avatar # User avatar component
│ ├───bookmarks # Bookmark component

│ ├───clock # Clock component

│ ├───device # Hardware information component

│ ├───quote # Quote

│ ├───search-box # Search box component

│ ├───trending-badges # Trending tags component

│ └───weather # Weather component

├───consts

│ └───weather # Mapping table between weather charts and corresponding county/city data sets

├───lib

│ ├───device-info # Hardware information API wrapper

│ ├───trending # Trending tags API wrapper

│ └───weather # Weather API wrapper

├───stores # Pinia status management (including weather, hardware information, shortcuts, etc.)

└───types # TypeScript type definitions (including weather, hardware information, shortcuts, etc.)

```

## Technology Stack

- **Front-end frameworks**: [Vue 3](https://vuejs.org/), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/)

- **State management**: [Pinia](https://pinia.vuejs.org/)

- **UI component library**: [shadcn-vue](https://shadcn-vue.com/)

- **API and data interaction**: [Browser Homepage Next/Server](https://github.com/510208/browser-homepage-next/tree/main/server), [personal-website-route](https://github.com/510208/personal-website-route)

- **Deployment and hosting**: [GitHub](https://github.com/510208/browser-homepage-next/tree/main/server), [personal-website-route](https://github.com/510208/personal-website-route)

- **Deployment and hosting**: [GitHub](https://github.com/510208/personal-website-route) Pages (https://pages.github.com/)

## Installation and Execution

This project requires a Node.js environment to run. Please install Node.js and pnpm first (fnm is recommended). After downloading the project, execute the following commands in the project root directory to install dependencies:

``bash

# Install fnm (if not already installed)

# https://github.com/Schniz/fnm

$ curl -fsSL https://fnm.vercel.app/install | bash # Linux/macOS

$ iwr https://fnm.vercel.app/install | iex # PowerShell (Windows)

# Install Node.js (if not already installed)

$ fnm install 24.3.0

$ fnm use 24.3.0

# Install pnpm via corepack (if not already installed)

$ npm install -g corepack

$ corepack enable pnpm

# Install project dependencies

$ pnpm install

# Start the development server

$ pnpm run dev

# --- or use antfu/ni ---

# Install antfu/ni (if not already installed)

# https://github.com/antfu-collective/ni

$ npm i -g @antfu/ni

# Install project dependencies

$ ni

# Start the development server

$ nr dev

```

> [!IMPORTANT]

> Ensure the [Server] (./server) is running

## Important Notes

> [!WARNING]

> Do not steal or misuse the APIs used in this project. The developer has restricted this.

>
> If needed, please deploy your own [API route](https://github.com/510208/personal-website-route) to provide API services. All APIs used in this project are free. Please respect the developer's hard work and efforts; do not steal or misuse them.

> [!WARNING]

> Static resources such as fonts and icons are all open-source or free materials. Please do not steal or use them commercially.

>
> However, the background images in this project are from the Internet. If there is any copyright infringement, please contact the developer for removal.

- Currently, the system's weather information is provided by the Central Weather Administration of the Republic of China (https://opendata.cwa.gov.tw/), and only supports weather information for counties and cities in Taiwan. If you are located in other countries or regions, please note that the weather information may not display correctly and may cause errors in your terminal.

- Please ensure that the [Server-side](./server) is running to provide the hardware information API; otherwise, hardware information will not display correctly.

- For any questions or suggestions, please submit them through [GitHub Issues](https://github.com/510208/browser-homepage-next/issues). The developers will respond and process them as soon as possible. If you are interested in participating in the project development, you are welcome to assist in the project development through [Pull Requests](https://github.com/510208/browser-homepage-next/pulls).

- This tool was originally written by the developer for their own use. We apologize for any shortcomings and welcome suggestions or assistance in improving it.

## Acknowledgements

- Thanks to the developers and communities of the various frameworks who provided excellent tools and resources, enabling the successful completion of this project.

- Thanks to Pixiv author [Bingwei 冰鲔](https://www.pixiv.net/users/32268297) for the illustration (https://www.pixiv.net/artworks/81639719), nice work!

- Thanks to the developers and organizations providing API services

- [Hitokoto 一言](https://developer.hitokoto.cn/sentence/)

- [personal-website-route](https://github.com/510208/personal-website-route)

- [Central Weather Administration](https://opendata.cwa.gov.tw/)

- Thanks to [LigHTTP工程项目](https://github.com/510208/lighttp) for providing excellent HTTP request testing tools to accelerate the development process

---

<div align="center">

<img height="60" src="https://api.moedog.org/count/@browser-homepage-next?theme=asoul" alt="Visitor Count Statistics" />

<br />
<small>Made by SamHacker | Built with ❤️</small>

</div>

```
