# Reproduce a Rails production build

Use a fresh disposable checkout or the application's build container. Start
from its build definition, version files and `Gemfile.lock`. Match the Ruby
version, the locked Bundler version and the target platform and dependency
groups. If the app builds JS or CSS separately, also use its declared toolchain
and lockfile install command. Keep generated output from earlier builds out of
the checkout.

## Check the lock and build output

This example uses Rails 8.1 and Propshaft with the default asset output path.
Use the app's declared build command and expected assets. The example stops
if local Bundler configuration overrides frozen mode. Asset tasks can run
application initializers, so use isolated build settings without production
credentials or live service endpoints.

```sh
(
  set -eu
  export BUNDLE_FROZEN=true
  ruby -v
  bundle --version
  if [ "$(bundle config get --parseable frozen)" != "frozen=true" ]; then
    printf '%s\n' 'Bundler frozen mode is required. Check local Bundler settings.' >&2
    exit 1
  fi
  bundle install
  bundle exec bin/rails --version
  RAILS_ENV=production SECRET_KEY_BASE_DUMMY=1 bundle exec bin/rails assets:precompile

  ruby -rjson - public/assets application.css <<'RUBY'
directory, logical_name = ARGV
manifest = JSON.parse(File.read(File.join(directory, ".manifest.json")))
entry = manifest[logical_name]
filename = entry.is_a?(Hash) ? entry["digested_path"] : entry
path = File.join(directory, filename) if filename.is_a?(String)
abort "Missing compiled asset: #{logical_name}" unless path && File.file?(path) && File.size?(path)
puts "Built #{logical_name} as #{filename}"
RUBY
)
```

Use the deployed pipeline's manifest format and output path. For an app without
an asset pipeline, mark precompile inapplicable and run its own build checks.
`SECRET_KEY_BASE_DUMMY` supplies a temporary Rails key for precompilation.
If an initializer still needs configuration, use the app's isolated build
settings or report the blocked stage.
[Bundler configuration](https://guides.rubygems.org/command-reference/bundle-config/) ·
[Rails 8.1 asset pipeline](https://guides.rubyonrails.org/v8.1/asset_pipeline.html#precompiling-assets)

## Report the evidence

Record the versions, command and expected artifacts, and report which stage
failed or was skipped. A successful build shows that the selected environment
produced those artifacts. To claim configured readiness, boot with the intended
configuration in an authorized environment and exercise a representative route
and its required dependencies. Report that separately from the build result.
