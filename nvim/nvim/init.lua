-- ==========================================
-- ⚙️ Neovim Laravel + Oil + NeoTree + Lualine + Telescope + Emmet (Tab expand)
-- ==========================================

vim.g.mapleader = " "
vim.opt.number = true
vim.opt.termguicolors = true
vim.opt.expandtab = true
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.clipboard = "unnamedplus"

-- ==========================================
-- 📦 Lazy.nvim setup
-- ==========================================
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.uv.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- ==========================================
-- 🧩 Plugins
-- ==========================================
require("lazy").setup({

  -- Laravel.nvim
  {
    "adalessa/laravel.nvim",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-telescope/telescope.nvim",
      "MunifTanjim/nui.nvim",
      "nvim-neotest/nvim-nio",
    },
    config = function()
      require("laravel").setup({
        artisan = { command = "php artisan", use_sail = false },
        routes = { enable = true },
        completion = { enable = true },
      })
      print("✅ Laravel.nvim cargado correctamente 🚀")
    end,
  },

  -- Oil.nvim
  {
    "stevearc/oil.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("oil").setup({ view_options = { show_hidden = true } })
      vim.keymap.set("n", "<leader>o", ":Oil<CR>", { desc = "Abrir Oil" })
    end,
  },

  -- Neo-tree.nvim
  {
    "nvim-neo-tree/neo-tree.nvim",
    branch = "v3.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-tree/nvim-web-devicons",
      "MunifTanjim/nui.nvim",
    },
    config = function()
      require("neo-tree").setup({
        close_if_last_window = true,
        filesystem = {
          filtered_items = {
            visible = true,
            hide_dotfiles = false,
            hide_gitignored = false,
          },
        },
      })
      vim.keymap.set("n", "<leader>e", ":Neotree toggle left<CR>", { desc = "Abrir Neo-tree" })
    end,
  },

  -- Treesitter (sintaxis moderna)
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function()
      require("nvim-treesitter.configs").setup({
        ensure_installed = { "lua", "html", "css", "javascript", "json", "php" },
        highlight = { enable = true },
        auto_install = true,
      })
    end,
  },

  -- Telescope (buscador tipo VSCode)
  {
    "nvim-telescope/telescope.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require("telescope").setup({
        defaults = {
          layout_strategy = "vertical",
          layout_config = { preview_cutoff = 20 },
        },
      })
      vim.keymap.set("n", "<leader>p", ":Telescope find_files<CR>", { desc = "Buscar archivos" })
      vim.keymap.set("n", "<leader>f", ":Telescope live_grep<CR>", { desc = "Buscar texto" })
    end,
  },

  -- Barra inferior tipo VSCode
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("lualine").setup({
        options = {
          theme = "auto",
          section_separators = "",
          component_separators = "",
          icons_enabled = true,
        },
      })
    end,
  },

  -- Emmet (Tab expand como VSCode)
  {
    "mattn/emmet-vim",
    config = function()
      vim.g.user_emmet_mode = "a"             -- habilitado para todos los modos
      vim.g.user_emmet_install_global = 0     -- evitar conflictos globales
      vim.cmd([[
        autocmd FileType html,css,astro,vue,jsx,tsx,typescriptreact EmmetInstall
      ]])
    end,
  },

  -- LSP + Autocompletado
  { "williamboman/mason.nvim", config = true },
  { "williamboman/mason-lspconfig.nvim" },
  { "neovim/nvim-lspconfig" },
  { "hrsh7th/nvim-cmp" },
  { "hrsh7th/cmp-nvim-lsp" },
  { "L3MON4D3/LuaSnip" },
  { "saadparwaiz1/cmp_luasnip" },
})

-- ==========================================
-- ⚙️ LSP limpio (Neovim 0.11 compatible)
-- ==========================================
require("mason-lspconfig").setup({
  ensure_installed = { "intelephense" },
})

local capabilities = require("cmp_nvim_lsp").default_capabilities()
vim.lsp.config("intelephense", {
  capabilities = capabilities,
  cmd = { "intelephense", "--stdio" },
  filetypes = { "php" },
  root_dir = vim.fs.root(0, { "composer.json", ".git" }),
})
vim.lsp.enable("intelephense")

-- ==========================================
-- ✨ Autocompletado con Tab (inteligente + Emmet)
-- ==========================================
local cmp = require("cmp")
local luasnip = require("luasnip")

local has_words_before = function()
  local line, col = unpack(vim.api.nvim_win_get_cursor(0))
  return col ~= 0 and vim.api.nvim_buf_get_lines(0, line - 1, line, true)[1]:sub(col, col):match("%s") == nil
end

cmp.setup({
  snippet = { expand = function(args) luasnip.lsp_expand(args.body) end },
  mapping = {
    ["<Tab>"] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_next_item()
      elseif luasnip.expand_or_jumpable() then
        luasnip.expand_or_jump()
      elseif has_words_before() then
        cmp.complete()
      else
        fallback() -- Si no hay nada, Tab expande Emmet
      end
    end, { "i", "s" }),
    ["<S-Tab>"] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_prev_item()
      elseif luasnip.jumpable(-1) then
        luasnip.jump(-1)
      else
        fallback()
      end
    end, { "i", "s" }),
    ["<CR>"] = cmp.mapping.confirm({ select = true }),
  },
  sources = cmp.config.sources({
    { name = "nvim_lsp" },
    { name = "luasnip" },
  }),
})

-- ==========================================
-- 🪟 Movimiento entre ventanas tipo VSCode
-- ==========================================
vim.keymap.set("n", "<C-h>", "<C-w>h")
vim.keymap.set("n", "<C-l>", "<C-w>l")
vim.keymap.set("n", "<C-j>", "<C-w>j")
vim.keymap.set("n", "<C-k>", "<C-w>k")
vim.keymap.set("n", "<leader>sv", ":vsplit<CR>")
vim.keymap.set("n", "<leader>sh", ":split<CR>")
vim.keymap.set("n", "<leader>sc", ":close<CR>")

print("✅ Laravel.nvim + Oil + Neo-tree + Telescope + Lualine + Emmet(Tab) listos 🚀")
