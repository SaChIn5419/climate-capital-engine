/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  basePath: "/climate-capital-engine",
  assetPrefix: "/climate-capital-engine/",
  images: { unoptimized: true },
  trailingSlash: true,
  eslint: { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors: true },
};
module.exports = nextConfig;
