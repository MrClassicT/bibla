---
layout: page
title: Home
permalink: /
---

# Index

`bibla` is a simple, lightweight, and fast bibliography linter. It is designed to help you keep your bibliography files clean and consistent. bibla is written in Python and is available as a command-line tool. It's based on [`bibl`](https://gitlab.com/arnevdk/bibl) by Arne Van Den Kerckhove, but with the adaptations and extensions to work for BibLaTeX files.

To get started, make sure you have Python installed and pip. Simply use the following pip command to install `bibla`:

```bash
pip install bibla
```

After installing bibla, you can lint your bibliography files by running the following command:

```bash
bibla lint <path-to-your-file.bib>
```

If you wish to view an overview of all the implemented rules, you can either use the `bibla --help` command or visit the [documentation](/bibla/docs/overview/).

It's good to note that the rules are slightly oppinionated towards the likings of HOGENT lecturers, since the request for this tool came from them. Due to the open source nature of the project, you can always fork and adapt rules to your own liking.

If you have any questions, suggestions, or issues, feel free to reach out. You can find my contact information on the [Contact](/bibla/contact/) page.

In case you're interested in the source code, you can find it on [GitLab](https://gitlab.com/MrClassicT/bibla). If you wish to contribute, feel free to create a pull-request.

Enjoy using `bibla`!

For those wondering about the reason why I created this tool, this is a proof of concept for my bachelor's thesis. If you're interested in reading it, you can find it [here](/bibla/thesis). **Please note**: it's written in Dutch and not available in English!

The source code of `bibla` is available at [Github](https://github.com/MrClassicT/bibla).