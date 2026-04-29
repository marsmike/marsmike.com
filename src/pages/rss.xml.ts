import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts', ({ data }) => data.lang === 'de' && data.status === 'live'))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  return rss({
    title: 'marsmike.com',
    description: 'Mike Müller — Software-Delivery im GenAI-Zeitalter.',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.summary,
      pubDate: post.data.date,
      link: `/posts/${post.slug.replace(/^de\//, '')}/`,
    })),
    customData: '<language>de-DE</language>',
  });
}
