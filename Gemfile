source 'https://rubygems.org'

gem 'jekyll', '~> 4.3.2'
gem 'jekyll-feed', '~> 0.17.0'
gem 'jekyll-sitemap', '~> 1.4.0'
gem 'jekyll-seo-tag', '~> 2.8.0'
gem 'jekyll-paginate-v2', '~> 3.0.0'
gem 'webrick', '~> 1.8.1'
gem 'tzinfo-data', '~> 1.2023.3'

group :jekyll_plugins do
  gem 'jekyll-postcss', '~> 0.5.0'
  gem 'jekyll-minifier', '~> 0.1.10'
end

platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem 'tzinfo', '>= 1', '< 3'
end

platforms :ruby do
  gem 'wdm', '>= 0.1.1' if Gem.win_platform?
end
