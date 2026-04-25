using System.Net.Http.Json;

namespace BeccaMaePortfolio.Services;

public class FolderManifest
{
    public string Name { get; set; } = "";
    public string Title { get; set; } = "";
    public string Thumbnail { get; set; } = "";
    public List<string> Images { get; set; } = new();
}

public class ImageService(HttpClient http)
{
    private List<FolderManifest>? _cache;

    public async Task<List<FolderManifest>> GetFoldersAsync()
    {
        _cache ??= await http.GetFromJsonAsync<List<FolderManifest>>("images/manifest.json") ?? new();
        return _cache;
    }

    public async Task<FolderManifest?> GetFolderAsync(string name)
    {
        var folders = await GetFoldersAsync();
        return folders.FirstOrDefault(f => f.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
    }
}
