technologies = [
    ['python', 'py', 'py2', 'py3'],
    ['golang', ' go,'],  # some likelihood for false positives
    [' java'],
    ['php'],
    ['django'],
    ['ruby', 'ruby on rails'],
    ['javascript'],
    ['c ', 'c,'],  # some likelihood for false positives
    ['c++'],
    [' rust'],
    ['c#'],
    ['typescript'],
    ['symphony'],
    ['laravel'],
    ['nodejs', 'node', 'node.js'],
    ['angular'],
    ['react'],
    ['swift'],
    ['perl'],
    ['html', 'css'],
    ['flask'],
    ['fastapi'],
    ['vue', 'vue.js', 'vuejs'],
    ['express', 'expressjs'],
    ['cakephp'],
    ['asp.net', ' .net'],
    ['koa'],
    ['phoenix'],
    ['spring'],
    ['aws'],
    ['git'],
    ['azure'],
    ['gcp'],
    ['fiber'],
    ['scala']
]
stats = {
    'technologies': {},
    'companies': {}
}


def process_data(job_post):
    process_technologies(job_post.company, job_post.description.lower())
    save_job_post(job_post)


def save_job_post(job_post):
    with open('all_job_posts.json', 'a') as f:
        blob = f'- Company: {job_post.company} -- Insights: {job_post.insights} -- Description: {job_post.description}' \
               f'\n\n\n=============================================================\n' \
               f'=============================================================\n\n\n'
        f.write(blob)


def process_technologies(company, job_description):
    lower_description = job_description.lower()
    for technology_synonyms in technologies:
        if _is_tech_in_jd(technology_synonyms, lower_description):
            tech_slug = _build_tech_slug(technology_synonyms)
            _process_technologies_counter(tech_slug)
            _process_technologies_per_company(company, tech_slug)


def _process_technologies_counter(tech_slug):
    if stats['technologies'].get(tech_slug):
        stats['technologies'][tech_slug] += 1
    else:
        stats['technologies'][tech_slug] = 1


def _process_technologies_per_company(company, tech_slug):
    if stats['companies'].get(company):
        company_tech_list = stats['companies'][company]
        if tech_slug not in company_tech_list:
            company_tech_list.append(tech_slug)
        stats['companies'][company] = company_tech_list
    else:
        stats['companies'][company] = [tech_slug]


def _is_tech_in_jd(techs, description):
    found = False
    for tech in techs:
        if tech in description:
            found = True
            break
    return found


def _build_tech_slug(tech_synonyms):
    tech_slug = ''
    for idx, tech in enumerate(tech_synonyms):
        if idx == 0:
            tech_slug = tech
        else:
            tech_slug += '_' + tech
    return tech_slug
