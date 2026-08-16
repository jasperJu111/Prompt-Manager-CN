import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: '提示管理器-CN',
  description: '面向中文开发者与创作者的开源 AI 提示词库',
  base: '/Prompt-Manager-CN/',
  cleanUrls: true,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '提示词目录', link: '/prompts/' },
      { text: '使用指南', link: '/guide/getting-started' },
      { text: 'GitHub', link: 'https://github.com/jasperJu111/Prompt-Manager-CN' }
    ],
    sidebar: [
      {
        text: '开始使用',
        items: [
          { text: '项目介绍', link: '/' },
          { text: '快速开始', link: '/guide/getting-started' },
          { text: '贡献提示词', link: '/guide/contributing' }
        ]
      },
      {
        text: '提示词库',
        items: [{ text: '全部提示词', link: '/prompts/' }]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/jasperJu111/Prompt-Manager-CN' }
    ],
    footer: {
      message: '基于 MIT License 发布',
      copyright: 'Copyright © 2026 jasperJu111 and contributors'
    },
    search: { provider: 'local' }
  }
})
