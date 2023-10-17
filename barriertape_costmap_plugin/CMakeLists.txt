cmake_minimum_required(VERSION 3.8)
project(barriertape_costmap_plugin)

set(lib_name ${PROJECT_NAME}_core)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav2_costmap_2d REQUIRED)
find_package(pluginlib REQUIRED)

# You set a list of dependencies to make it more compact
set(dep_pkgs
    rclcpp
    nav2_costmap_2d
    pluginlib)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# === Build ===

add_library(${lib_name} SHARED
            src/barrier_layer.cpp)

include_directories(include)
# add_executable(barrier_tape_layer src/barrier_layer.cpp ${BEHAVIOR_SOURCES})
# ament_target_dependencies(barrier_tape_layer ${dep_pkgs})
# target_link_libraries(barrier_tape_layer ${YAML_CPP_LIBRARIES})


# === Installation ===

install(TARGETS ${lib_name}
        DESTINATION lib)
      
install(DIRECTORY include/
    DESTINATION include/
)
# === Ament work ===

# pluginlib_export_plugin_description_file() installs gradient_layer.xml
# file into "share" directory and sets ament indexes for it.
# This allows the plugin to be discovered as a plugin of required type.
pluginlib_export_plugin_description_file(nav2_costmap_2d barrier_layer.xml)
ament_target_dependencies(${lib_name} ${dep_pkgs})


ament_package()