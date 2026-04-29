import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts', ({ data }) => data.lang === 'en' && data.status === 'live'))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  return rss({
    title: 'marsmike.com',
    description: 'Mike Müller — software delivery in the GenAI era.',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.summary,
      pubDate: post.data.date,
      link: `/en/posts/${post.slug.replace(/^en\//, '')}/`,
    })),
    customData: '<language>en-US</language>',
  });
}
