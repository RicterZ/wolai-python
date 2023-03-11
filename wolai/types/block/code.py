from wolai.types.enum import AutoName, auto
from wolai.types.block import Block
from wolai.types.text import CreateRichText
from wolai.exceptions import WolaiEnumTypeException


class CodeLanguage(AutoName):
    text = auto()
    ybsz = auto()
    latex = auto()
    c = auto()
    r = auto()
    csharp = auto()
    go = auto()
    css = auto()
    xml = auto()
    html = auto()
    svg = auto()
    markup = auto()
    cpp = auto()
    elm = auto()
    git = auto()
    php = auto()
    bash = auto()
    dart = auto()
    flow = auto()
    java = auto()
    json = auto()
    rb = auto()
    rust = auto()
    yaml = auto()
    nginx = auto()
    clike = auto()
    dockerfile = auto()
    matlab = auto()
    python = auto()
    stylus = auto()
    graphql = auto()
    markdown = auto()
    js = auto()
    jsx = auto()
    tsx = auto()
    typescript = auto()
    sass = auto()
    scss = auto()
    objectivec = auto()
    swift = auto()
    vala = auto()
    vbnet = auto()
    scala = auto()
    visual__basic = auto()
    perl = auto()
    abap = auto()
    lua = auto()
    ada = auto()
    groovy = auto()
    julia = auto()
    haskell = auto()
    coffeescript = auto()
    elixir = auto()
    powershell = auto()
    clojure = auto()
    lisp = auto()
    vim = auto()
    ocaml = auto()
    erlang = auto()
    puppet = auto()
    fortran = auto()
    fsharp = auto()
    nix = auto()
    wasm = auto()
    ftl = auto()
    asm6502 = auto()
    qml = auto()
    sql = auto()
    basic = auto()
    makefile = auto()
    pascal = auto()
    scheme = auto()
    regex = auto()
    kotlin = auto()
    ini = auto()
    http = auto()
    verilog = auto()
    properties = auto()
    glsl = auto()
    dax = auto()
    tcl = auto()
    ignore = auto()
    protobuf = auto()
    nasm = auto()
    hlsl = auto()
    vhdl = auto()
    nim = auto()
    mermaid = auto()
    arduino = auto()
    processing = auto()
    batch = auto()
    excel__formula = auto()
    diff = auto()
    toml = auto()
    wolfram = auto()
    stata = auto()
    cypher = auto()


class CodeSetting:
    line_number: bool = False
    link_break: bool = False
    ligatures: bool = False
    preview_format: str = None

    def __init__(self, line_number: bool = False, link_break: bool = False, ligatures: bool = False,
                 preview_format: str = None):
        self.line_number = line_number
        self.link_break = link_break
        self.ligatures = ligatures

        if preview_format not in ('both', 'code', 'mermaid', None):
            raise WolaiEnumTypeException(f'unknown preview_format "{preview_format}"')

        self.preview_format = preview_format


class CodeBlock(Block):
    language: CodeLanguage = None
    code_setting: CodeSetting = None
    caption: str = None
    content: CreateRichText = None

    def __init__(self, language: CodeLanguage | str = 'text', code_setting: CodeSetting | str = None,
                 caption: str = '', content: CreateRichText = None, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        if isinstance(language, str):
            language = CodeLanguage[language]

        self.language = language
        self.code_setting = code_setting
        self.caption = caption

