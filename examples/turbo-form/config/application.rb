require "rails"
require "active_record/railtie"
require "action_controller/railtie"
require "rails/test_unit/railtie"

Bundler.require(*Rails.groups)

module TurboForm
  class Application < Rails::Application
    config.load_defaults 8.1
    config.eager_load = false
  end
end
