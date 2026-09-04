using System;
using System.Collections.Generic;

namespace FastApiBack;

public class Files
{
    protected string _filePath;
    public List<string> Filelist { get; set; } = new List<string>();

    public Files(string filePath)
    {
        this._filePath = filePath;
    }

    public List<string> ListFiles()
    {
        return this.Filelist;
    }

    public void Example()
    {
        Console.WriteLine("Files class initialized");
    }
}
