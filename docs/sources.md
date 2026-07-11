# Source Strategy

CareerPilot uses direct company sources where a stable, permitted public feed is available. It complements—not replaces—official job alerts. LinkedIn, Indeed, IrishJobs, and Jobs.ie are important discovery channels, but CareerPilot must not log into or scrape them.

## Target company career sites

Use each site to create an official alert for Ireland/Cork/remote roles with the search terms in `config/profile.yaml`.

| Employer | Career site | Recommended use |
|---|---|---|
| Apple | [Jobs at Apple](https://jobs.apple.com/en-ie/search) | Direct search and job alert/email where available |
| Analog Devices | [ADI careers](https://www.analog.com/en/about-adi/careers.html) | Direct search / talent community |
| Dell Technologies | [Dell Ireland jobs](https://jobs.dell.com/en/location/ireland-jobs/375-30225/2963597/2/1) | Direct search plus talent network |
| Johnson & Johnson | [J&J Ireland careers](https://www.careers.jnj.com/en/locations/emea/ireland/) | Direct search plus Talent Hub |
| Boston Scientific | [Boston Scientific jobs](https://jobs.bostonscientific.com/) | Direct job search / talent community |
| Stryker | [Stryker Ireland jobs](https://careers.stryker.com/jobs?filter%5Bcountry%5D%5B0%5D=Ireland) | Direct search plus talent community |
| BioMarin | [BioMarin Ireland jobs](https://careers.biomarin.com/location/ireland-jobs/5804/2963597/2) | Direct search and alert |
| Alcon | [Alcon careers](https://careers.alcon.com/) | Direct search / talent community |
| Qualcomm | [Qualcomm careers](https://careers.qualcomm.com/) | Direct search / job alert |
| Logitech | [Logitech careers](https://www.logitech.com/en-us/about/careers.html) | Direct search / job alert |
| Broadcom | [Broadcom careers](https://www.broadcom.com/company/careers) | Direct search |
| Intel | [Intel jobs](https://jobs.intel.com/) | Direct search / job alert |
| Microsoft | [Microsoft careers](https://careers.microsoft.com/) | Direct search / job alert |
| Amazon | [Amazon Jobs](https://www.amazon.jobs/) | Direct search / job alert |
| Schneider Electric | [Schneider Electric careers](https://www.se.com/ww/en/about-us/careers/) | Direct search |
| ESB | [ESB careers](https://www.esb.ie/careers) | Direct vacancy page / alert |
| UCC | [UCC vacancies](https://www.ucc.ie/en/hr/vacancies/) | Direct vacancy page |
| MTU | [MTU vacancies](https://www.mtu.ie/about-mtu/vacancies/) | Direct vacancy page |
| Tyndall | [Tyndall careers](https://www.tyndall.ie/careers/) | Direct vacancy page |
| Workday | [Workday careers](https://www.workday.com/en-us/company/careers.html) | Direct search / job alert |
| SmartBear | [SmartBear careers](https://smartbear.com/company/careers/) | Direct search / job alert |
| Trend Micro | [Trend Micro careers](https://www.trendmicro.com/en_us/about/careers.html) | Direct search / job alert |
| Zendesk | [Zendesk careers](https://jobs.zendesk.com/) | Direct search / job alert |

## Broad-market sources

Create saved searches and email alerts at LinkedIn Jobs, Indeed Ireland, IrishJobs, Jobs.ie, PublicJobs.ie, EURES, and relevant specialist recruiters (for example Morgan McKinley, Hays, Cpl, CareerWise, and Collins McNicholas). Route those emails to the `CareerPilot Job Alerts` Outlook folder.

## Outlook inbox ingestion

1. Create a folder named `CareerPilot Job Alerts` in the mailbox used for job alerts.
2. Create rules that move alerts from approved senders into that folder.
3. Create an Outlook app password if required, then set `CAREERPILOT_IMAP_USERNAME` and `CAREERPILOT_IMAP_PASSWORD` in `.env` locally or as GitHub repository secrets.
4. Set `sources[0].enabled: true` in `config/profile.yaml`.
5. Test with `careerpilot run --dry-run`; only then use `careerpilot run --send-email`.

Email ingestion reads only the configured folder in read-only mode. It does not send applications, alter messages, or access other folders.

