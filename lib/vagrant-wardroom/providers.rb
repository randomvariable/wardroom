# Copyright 2019 The Wardroom Authors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

require_relative 'providers/libvirt.rb'
require_relative 'providers/virtualbox.rb'

# Helper module for Wardroom
module VagrantWardroom
  # Helper modules for different Vagrant providers
  module Providers
    module_function

    def configure(conf, **params)
      VirtualBox.configure(conf, params)
      Libvirt.configure(conf, params)
    end
  end
end