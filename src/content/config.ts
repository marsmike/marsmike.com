import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string().max(200),
    date: z.coerce.date(),
    lang: z.enum(['de', 'en']),
    status: z.enum(['draft', 'live']).default('live'),
    tags: z.array(z.string()).default([]),
    linkedin_url: z.string().url().optional(),
    code_url: z.string().url().optional(),
    translation_of: z.string().optional(),
    artifacts: z.array(z.object({
      label: z.string(),
      url: z.string().url(),
      type: z.enum(['video', 'pdf', 'pptx', 'image', 'audio', 'other']).default('other'),
    })).default([]),
  }),
});

export const collections = { posts };
