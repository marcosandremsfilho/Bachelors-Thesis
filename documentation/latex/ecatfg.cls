\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{ecatfg}

% carrega a classe article 
\LoadClass[a4paper, 10pt, twocolumn]{article}

% pacotes requiridos
\RequirePackage[brazil]{babel}
\RequirePackage[T1]{fontenc}

\RequirePackage{amsmath, amsfonts, epsfig}
\RequirePackage{physics}
\RequirePackage[compact]{titlesec}
\RequirePackage{tabularx}
\RequirePackage{enumitem}
\RequirePackage{etoolbox}
\RequirePackage{subcaption}
\RequirePackage[size = small, figurename = Fig.]{caption}
\RequirePackage{bm}
\RequirePackage{hyperref}
\RequirePackage[left = 2cm, right = 2cm, bottom = 2.5cm, top = 2.5cm]{geometry}
\RequirePackage{float}
\RequirePackage{lmodern}
\RequirePackage{stfloats}
\RequirePackage{natbib}

\usepackage{graphicx}
\usepackage{url}
\urlstyle{same}


%espaçamento
\parskip 0ex plus 0.1ex minus 0.01ex
\abovedisplayskip 1.5ex plus 4pt minus 2pt
\belowdisplayskip \abovedisplayskip
\abovedisplayshortskip 0pt plus 4pt
\belowdisplayshortskip 0ex plus 4pt 
\setlength{\columnsep}{.5cm}
\setlength{\parindent}{.5cm}

% configuração do espaçamento das seções e subseções
\titlespacing{\section}{0pt}{1\baselineskip plus 0.2\baselineskip minus 0.2\baselineskip}{1\baselineskip plus 0.2\baselineskip minus 0.2\baselineskip}
\titlespacing{\subsection}{0pt}{1\baselineskip plus 0.2\baselineskip minus 0.2\baselineskip}{1\baselineskip plus 0.2\baselineskip minus 0.2\baselineskip}

% configuração do formato das seções e subseções
\titleformat{\section}{\scshape\large\centering}{\thesection}{.2cm}{}
\titleformat{\subsection}{\itshape}{\thesubsection}{.1cm}{}

% configuração da numeração das seções e subseções
\renewcommand{\thesection}{\Roman{section}}
\renewcommand{\thesubsection}{\Roman{section}.\arabic{subsection}}

\newcommand{\titulo}[1]{\def \Titulo{#1}}
\newcommand{\autor}[1]{\def \Autor{#1}}
\newcommand{\data}[1]{\def \Data{#1}}
\newcommand{\orientador}[1]{\def \Orientador{#1}}
\newcommand{\coorientador}[1]{\def \Coorientador{#1}}
\newcommand{\resumo}[1]{\def \Resumo{#1}}
\newcommand{\palavrasChave}[1]{\def \Keywords{#1}}

\newcommand{\imprimirCabecalho}{
	\twocolumn[
	\begin{minipage}{0.2\linewidth}
		\includegraphics{Figuras/logo_converted_matched_size.pdf}
	\end{minipage}
	\begin{minipage}{0.8\linewidth}
		\scshape\Large
		\begin{flushright}	
			\begin{tabular}{c}
				Trabalho Final de Graduação -- \Data \\
				Universidade Federal de Itajubá \\
				Engenharia de Controle e Automação
			\end{tabular}
		\end{flushright}
	\end{minipage}
	
	\vspace{1.54\baselineskip}
	\begin{center}
		\MakeUppercase{\bf\Large \Titulo} \\\vspace{1.04\baselineskip}
		
		\large{\bfseries \Autor} \\\vspace{1.04\baselineskip}
		
		\ifcsdef{Coorientador}{
			\normalsize Orientador: \Orientador \\
			Coorientador: \Coorientador
		}{
			\normalsize Orientador: \Orientador
		}
	\end{center}
	\vspace{1.54\baselineskip}
	]
}

\newcommand{\imprimirResumo}{
	{\small\bfseries Resumo: \Resumo
		
	Palavras-Chave: \Keywords}
}

% comando que altera o ambiente matrix e alinha as colunas da forma desejada: centralizada, alinhada à esquerda ou alinhada à direita.
\makeatletter
\renewcommand*\env@matrix[1][c]{\hskip -\arraycolsep
	\let\@ifnextchar\new@ifnextchar
	\array{*\c@MaxMatrixCols #1}}
\makeatother

% configuração do ambiente enumerate de primeiro nível
\setlist[enumerate, 1]{leftmargin = .55cm, itemsep = 1pt, parsep = 1pt}

% alteração das fontes bold
\renewcommand{\bfdefault}{b}

