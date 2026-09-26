from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
def ident(value): return hashlib.sha1(value.encode()).hexdigest()[:24].upper()
def quote(s): return '"'+str(s).replace('"','\\"')+'"'
files=sorted((ROOT/'FoldAndFetch').rglob('*.swift'))
resources=sorted(p for p in (ROOT/'FoldAndFetch/Resources/AssetContent').iterdir() if p.is_file())
objects=[]
def obj(key,body): objects.append(f'{ident(key)} = {{ {body} }};'); return ident(key)
source_refs=[];resource_refs=[];source_build=[];resource_build=[]
for p in files+resources:
 rel=p.relative_to(ROOT).as_posix();kind='sourcecode.swift' if p.suffix=='.swift' else {'.scn':'file.scn','.png':'image.png','.json':'text.json','.wav':'audio.wav'}.get(p.suffix,'file')
 ref=obj('ref:'+rel,f'isa = PBXFileReference; lastKnownFileType = {quote(kind)}; path = {quote(rel)}; sourceTree = "<group>";')
 build=obj('build:'+rel,f'isa = PBXBuildFile; fileRef = {ref};')
 (source_refs if p.suffix=='.swift' else resource_refs).append(ref);(source_build if p.suffix=='.swift' else resource_build).append(build)
product=obj('product','isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = CorgiCrossroads.app; sourceTree = BUILT_PRODUCTS_DIR;')
def ids(xs): return ', '.join(xs)+(',' if xs else '')
sources=obj('sourcesGroup',f'isa = PBXGroup; children = ({ids(source_refs)}); name = Sources; sourceTree = "<group>";')
resgroup=obj('resourcesGroup',f'isa = PBXGroup; children = ({ids(resource_refs)}); name = AssetContent; sourceTree = "<group>";')
products=obj('products',f'isa = PBXGroup; children = ({product},); name = Products; sourceTree = "<group>";')
main=obj('mainGroup',f'isa = PBXGroup; children = ({sources},{resgroup},{products},); sourceTree = "<group>";')
sp=obj('sourcesPhase',f'isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = ({ids(source_build)}); runOnlyForDeploymentPostprocessing = 0;')
rp=obj('resourcesPhase',f'isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = ({ids(resource_build)}); runOnlyForDeploymentPostprocessing = 0;')
fp=obj('frameworksPhase','isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
configs=[];pconfigs=[]
for name in ['Debug','Release']:
 settings={'PRODUCT_NAME':'CorgiCrossroads','PRODUCT_BUNDLE_IDENTIFIER':'com.corgicrossroads.demo','SWIFT_VERSION':'5.0','IPHONEOS_DEPLOYMENT_TARGET':'27.1','TARGETED_DEVICE_FAMILY':'1,2','GENERATE_INFOPLIST_FILE':'YES','INFOPLIST_KEY_CFBundleDisplayName':'Corgi Crossroads','INFOPLIST_KEY_UIApplicationSceneManifest_Generation':'YES','INFOPLIST_KEY_UILaunchScreen_Generation':'YES','INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone':'UIInterfaceOrientationPortrait','INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad':'UIInterfaceOrientationPortrait','INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents':'YES','ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS':'NO','CODE_SIGN_STYLE':'Automatic','CODE_SIGNING_ALLOWED':'NO','CURRENT_PROJECT_VERSION':'1','MARKETING_VERSION':'1.0','LD_RUNPATH_SEARCH_PATHS':'$(inherited) @executable_path/Frameworks','SWIFT_OPTIMIZATION_LEVEL':'-Onone' if name=='Debug' else '-O','SWIFT_ACTIVE_COMPILATION_CONDITIONS':'DEBUG' if name=='Debug' else ''}
 body=' '.join(f'{k} = {quote(v)};' for k,v in settings.items())
 configs.append(obj('target'+name,f'isa = XCBuildConfiguration; buildSettings = {{ {body} }}; name = {name};'))
 pconfigs.append(obj('project'+name,f'isa = XCBuildConfiguration; buildSettings = {{ SDKROOT = iphoneos; CLANG_ENABLE_MODULES = YES; CLANG_ENABLE_OBJC_ARC = YES; DEBUG_INFORMATION_FORMAT = dwarf; }}; name = {name};'))
tl=obj('targetConfigs',f'isa = XCConfigurationList; buildConfigurations = ({ids(configs)}); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;')
pl=obj('projectConfigs',f'isa = XCConfigurationList; buildConfigurations = ({ids(pconfigs)}); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;')
target=obj('target',f'isa = PBXNativeTarget; buildConfigurationList = {tl}; buildPhases = ({sp},{fp},{rp},); buildRules = (); dependencies = (); name = CorgiCrossroads; productName = CorgiCrossroads; productReference = {product}; productType = "com.apple.product-type.application";')
project=obj('project',f'isa = PBXProject; attributes = {{ BuildIndependentTargetsInParallel = YES; LastUpgradeCheck = 2710; }}; buildConfigurationList = {pl}; compatibilityVersion = "Xcode 14.0"; developmentRegion = en; hasScannedForEncodings = 0; knownRegions = (en,Base,); mainGroup = {main}; productRefGroup = {products}; projectDirPath = ""; projectRoot = ""; targets = ({target},);')
folder=ROOT/'CorgiCrossroads.xcodeproj';folder.mkdir(exist_ok=True)
(folder/'project.pbxproj').write_text('// !$*UTF8*$!\n{ archiveVersion = 1; classes = {}; objectVersion = 56; objects = {\n'+'\n'.join(objects)+f'\n}}; rootObject = {project}; }}\n')
scheme=folder/'xcshareddata/xcschemes';scheme.mkdir(parents=True,exist_ok=True)
buildable=f'<BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{target}" BuildableName="CorgiCrossroads.app" BlueprintName="CorgiCrossroads" ReferencedContainer="container:CorgiCrossroads.xcodeproj"/>'
(scheme/'CorgiCrossroads.xcscheme').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="2710" version="1.3"><BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries><BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">{buildable}</BuildActionEntry></BuildActionEntries></BuildAction><TestAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" shouldUseLaunchSchemeArgsEnv="YES"><Testables/></TestAction><LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugDocumentVersioning="YES" debugServiceExtension="internal" allowLocationSimulation="YES"><BuildableProductRunnable runnableDebuggingMode="0">{buildable}</BuildableProductRunnable></LaunchAction><ProfileAction buildConfiguration="Release" shouldUseLaunchSchemeArgsEnv="YES" useCustomWorkingDirectory="NO" debugDocumentVersioning="YES"><BuildableProductRunnable runnableDebuggingMode="0">{buildable}</BuildableProductRunnable></ProfileAction><AnalyzeAction buildConfiguration="Debug"/><ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/></Scheme>''')
print(f'Project: {len(files)} Swift files, {len(resources)} resources')
