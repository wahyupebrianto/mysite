source "https://rubygems.org"

# Jekyll is built by GitHub Actions (see .github/workflows/deploy.yml), so any
# gem/plugin is allowed - we are NOT limited to the "github-pages" gem.
gem "jekyll", "~> 4.4"

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-redirect-from", "~> 0.16"
end

# Link / image / script checker used by CI and `scripts/check`.
group :test do
  gem "html-proofer", "~> 5.0"
end

# Needed by `jekyll serve` on Ruby >= 3.0
gem "webrick", "~> 1.9"

# Windows / JRuby helpers
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end
gem "wdm", "~> 0.2", platforms: [:mingw, :x64_mingw, :mswin]
