# 转转

<p align="center">
  <img src="Assets/app-preview.png" width="128" alt="转转应用图标">
</p>

Windows x64 portable 工具，可直接从文件、项目文件夹或 `ZIP`、`7Z`、`RAR` 压缩包识别 CATIA 原文件，并通过本机 CATIA V5 自动化接口批量导出为 STEP、IGES、STL、3DXML、CGR、VRML 或 CATIA V4 MODEL。

## 下载

从 [GitHub Releases](https://github.com/YESdontASKmeAgain-Engineer/CatiaStepConverter/releases) 下载最新的 `portable-win-x64.zip`，解压后保持 EXE 与同级依赖文件在一起，并可使用同一版本附带的 `SHA256SUMS.txt` 校验文件完整性。

## 功能

- 批量处理 `CATPart`、`CATProduct` 和 CATIA V4 `.model`。
- 支持 STEP AP242、IGES、STL、3DXML、CGR、VRML 和 CATIA V4 MODEL。
- 从文件名、项目目录或压缩包模糊识别碳板和 CNC 原文件。
- 在后台扫描目录和展开压缩包，耗时操作可随时取消。
- 通过独立后台 CATIA 会话执行转换，不退出用户已打开的 CATIA。
- 校验导出文件；STEP 会进一步读取并显示实际 `FILE_SCHEMA`。

## 使用

1. 双击 `转转.exe`，把 `CATPart`、`CATProduct`、`.model`、`ZIP`、`7Z` 或 `RAR` 文件拖入窗口。
2. 也可以把项目文件夹直接拖入窗口（或点击“选择文件夹”）。程序会在后台递归扫描文件夹和压缩包，并根据文件名和目录名模糊识别“碳板”和“CNC”原文件；`DEVICE`、`PLASTIC` 等未识别目录中的普通 CATIA 文件不会进入列表。扫描或解压期间可点击“取消”。
3. 勾选本次要转换的“碳板”和/或“CNC”，选择导出格式，再选择输出到源文件旁或统一目录；需要替换旧文件时勾选“覆盖同名文件”。手动加入的未分类文件始终保留在本次转换中。选择“源文件旁”时，压缩包内文件会输出到压缩包所在目录的 `<压缩包名>_导出` 文件夹。
4. 点击“开始转换”。未勾选类别或不兼容所选格式的文件不会提交给 CATIA，其它文件会显示转换结果；STEP 还会显示实际导出的 AP 标准。

自动识别的制造文件会在输出名称中加入类别后缀，例如 `支架_CNC.stp` 和 `侧板_碳板.stp`；手动添加的未分类文件保留原名称。同一输出目录中仍有重名时，程序会继续追加 `__2`、`__3`。

也可以直接把多个 CATIA 文件、压缩包或项目文件夹拖到 EXE 图标上。程序会自动识别并启动转换，默认导出 STEP AP242 且不覆盖已有文件。

模糊识别支持文件名和目录名中的 `CARBON`、`CFRP`、`碳板`、`碳纤`、`CNC`、`MACHINING`、`MACHINED`、`机加`、`机械加工`、`数控` 等关键词，不区分大小写，并忽略空格、下划线和连字符。例如 `01-carbon-parts`、`main-deck-carbon-v2.CATPart`、`2026-machining` 和 `fixture_cnc_revA.CATPart` 都可识别。目录分类优先于文件名；同一名称同时出现碳板和 CNC 关键词时保持未分类，避免误判。需要转换其它未分类文件时，请通过“选择文件”或直接拖入文件来添加。

程序会把压缩包完整解压到 EXE 同级的 `CatiaStepConverter.Archives` portable 工作区，保证 `CATProduct` 能继续找到同包内的引用零件；列表仍只加入识别出的碳板和 CNC 文件。移除该压缩包的最后一个列表项目、清空列表或关闭程序时，工作区会自动删除。程序意外退出时留下的工作区会在超过 24 小时且确认没有其它实例占用后自动清理。加密或带密码的压缩包不受支持，并会显示明确错误。

解压过程会拒绝绝对路径、越界路径、链接和重复目标，并限制为最多 20,000 个项目、单文件 5 GB、总展开大小 20 GB。

导出格式包括 `STEP (.stp)`、`IGES (.igs)`、`STL (.stl)`、`3DXML (.3dxml)`、`CGR (.cgr)`、`VRML (.wrl)` 和 `CATIA V4 MODEL (.model)`。经本机 CATIA V5 验证，STL 和 V4 MODEL 仅适用于 `CATPart`；选择这两种格式时，`CATProduct` 和 `.model` 输入会自动排除并在状态栏提示。其它五种格式可用于当前支持的零件和装配输入。

## 运行条件

- Windows 10/11 x64
- 本机已安装并正确注册 CATIA V5
- CATIA 许可证包含所需的 STEP 导出能力
- `CATProduct` 的引用零件可被 CATIA 正常找到

选择 STEP 时，程序会优先使用本机 CATIA 支持的最高 AP242 版本。CATIA V5-6R2023 可生成 AP242 Edition 3；程序还会读取输出文件的 `FILE_SCHEMA` 进行结果校验。批处理期间修改的 CATIA STEP 设置会在结束时恢复。其它格式会校验 CATIA 是否生成了有效的非空文件。

每个转换批次使用独立的后台 CATIA 会话，避免用户当前打开的 CATIA 处于编辑命令、长期运行或异常状态时影响批量导出。程序只会关闭自己创建的后台会话，不会退出用户已有的 CATIA 窗口。

## 构建

需要 [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)。源码仓库不包含 CATIA 或达索系统的任何二进制文件。

```powershell
dotnet publish .\CatiaStepConverter.csproj -c Release -r win-x64 --self-contained true -o .\publish
```

`publish` 目录是完整的 portable 文件夹，不要求目标机安装 .NET。请保持 EXE 与发布目录内的 DLL、运行库文件在一起；程序自己的工作区只会创建在 EXE 同级，不会写入 `AppData`、`LocalAppData` 或 `Roaming`。

推送形如 `v1.4.1` 的版本标签后，GitHub Actions 会先运行完整测试和格式检查，再自动发布 portable ZIP 与 SHA-256 校验文件：

```powershell
git tag v1.4.1
git push origin v1.4.1
```

## 测试

发现、安全、取消、临时工作区和 STEP Schema 测试不要求安装 CATIA，但 7Z 集成测试需要本机 `C:\Program Files\7-Zip\7z.exe`。

```powershell
dotnet run --project .\Tests\DiscoveryTests.csproj -c Release
dotnet run --project .\Tests\UiLogicTests.csproj -c Release
dotnet format .\CatiaStepConverter.csproj --verify-no-changes --no-restore
dotnet build .\CatiaStepConverter.csproj -c Release --no-restore
```

## 许可

项目代码采用 [MIT License](LICENSE) 开源。第三方依赖信息见 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)。

本项目与 Dassault Systemes 无隶属或背书关系；CATIA 是其权利人的商标。使用者需自行取得有效的 CATIA 软件和许可。
