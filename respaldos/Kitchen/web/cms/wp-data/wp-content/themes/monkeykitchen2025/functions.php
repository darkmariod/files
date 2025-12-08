<?php

function monkey_kitchen_setup(){
    add_theme_support('post-thumbnails');
}
add_action('after_setup_theme', 'monkey_kitchen_setup');